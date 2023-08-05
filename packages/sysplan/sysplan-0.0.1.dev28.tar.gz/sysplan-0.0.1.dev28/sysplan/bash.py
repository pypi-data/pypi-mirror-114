import asyncio
import shlex
import sys

from .colors import colors
from .plan import Plan


def transpile(src, prefix=None, output=None):
    output = output or []
    prefix = prefix or ''

    if isinstance(src, dict):
        for key, value in src.items():
            prefix_key = key
            if prefix:
                prefix_key = '_'.join([prefix, key])
            output = transpile(value, prefix_key, output)
    elif isinstance(src, list):
        for num, value in enumerate(src):
            output = transpile(value, f'{prefix}_{num}', output)
    elif isinstance(src, int):
        output.append(f'{prefix}={src}')
    elif isinstance(src, str):
        output.append(f'{prefix}={shlex.quote(src)}')

    return output


class BashPlan(Plan):
    def content(self):
        with open(self.path, 'r') as f:
            return f.read()

    async def write(self):
        return await self.call('write')

    async def activate(self):
        return await self.call('activate')

    async def diff(self):
        return await self.call('diff')

    async def destroy(self):
        return await self.call('destroy')

    async def call(self, function):
        variables = [
            f'plan_name="{self.name}"',
        ]
        variables += transpile(self)
        content = '\n'.join(variables) + f'\n{self.content()}\n{function}\n'
        print(''.join([
            colors['gray2bold'],
            f'+ {self.name} {function}',
            colors['reset'],
        ]))
        proc = await asyncio.create_subprocess_exec(
            '/bin/bash',
            '-c',
            content,
            stdout=sys.stdout,
            stderr=sys.stderr,
        )

        stdout, stderr = await proc.communicate()
        return (stdout or b'').decode('utf8') + (stderr or b'').decode('utf8')
