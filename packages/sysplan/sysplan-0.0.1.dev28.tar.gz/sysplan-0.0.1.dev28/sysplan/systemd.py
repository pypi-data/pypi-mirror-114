from pathlib import Path
import os

from .files import FilePlan
from .cli import context
from .run import run


class SystemdPlan(FilePlan):
    def path(self):
        return Path(os.path.join(
            self.root,
            'etc/systemd/sysplan',
            f'{self.name}.{self.ext}',
        ))

    def content(self):
        output = []
        for section_name, section_data in self.items():
            if len(output):
                output.append('')  # newline except on first line

            output.append(f'[{section_name}]')

            for key, value in section_data.items():
                output.append(f'{key}={value}')
        return '\n'.join(output)

    async def write(self):
        diff = await super().write()
        if diff:
            ctx = context.get(dict())
            ctx['systemd_reload'] = True
            context.set(ctx)
        return diff

    async def is_active(self):
        proc = await run(
            f'systemctl is-active {self.name}.{self.ext}',
            verbose=False,
        )
        return proc.returncode == 0

    async def is_enabled(self):
        proc = await run(
            f'systemctl is-enabled {self.name}.{self.ext}',
            verbose=False,
        )
        return proc.returncode == 0

    async def activate(self):
        ctx = context.get(dict())
        if 'systemd_reload' in ctx:
            del ctx['systemd_reload']
            context.set(ctx)
            await run('sudo systemctl daemon-reload')
        if not await self.is_enabled():
            await run(f'systemctl enable {self.root}/{self.name}.{self.ext}')

    async def destroy(self):
        if await self.is_enabled():
            await run(f'systemctl disable {self.name}.{self.ext}')
        if await self.is_active():
            await run(f'systemctl stop {self.name}.{self.ext}')
        await super().destroy()

    async def start(self):
        if not await self.is_active():
            await run(f'systemctl start {self.name}.{self.ext}')


class MountPlan(SystemdPlan):
    ext = 'mount'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setdefault('Install', dict())
        self['Install'].setdefault('WantedBy', 'multi-user.target')
        self.setdefault('Unit', dict())
        self['Unit'].setdefault('Description', f'{self.name} Timer')

    async def activate(self):
        await super().activate()
        await self.start()


class TimerPlan(SystemdPlan):
    ext = 'timer'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setdefault('Install', dict())
        self['Install'].setdefault('WantedBy', 'timers.target')
        self.setdefault('Unit', dict())
        self['Unit'].setdefault('Description', f'{self.name} Timer')

    async def activate(self):
        await super().activate()
        await self.start()


class ServicePlan(SystemdPlan):
    ext = 'service'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setdefault('Install', dict())
        self['Install'].setdefault('WantedBy', 'multi-user.target')
        self.setdefault('Unit', dict())
        self['Unit'].setdefault('Description', f'{self.name} Timer')
        self.setdefault('Service', {})
        env = {}
        for section_name, section_data in self.items():
            if section_name.upper() == section_name:
                env[section_name] = section_data
                continue

        if env:
            for name in env:
                del self[name]
            self['Service'].setdefault('Environment', '')
            for envname, envvalue in env.items():
                self['Service']['Environment'] += f' {envname}={envvalue}'
            self['Service']['Environment'].strip()

    async def activate(self):
        await super().activate()
        if self.name in self.config.get('timers', {}):
            await self.start()
