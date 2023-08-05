from pathlib import Path
import os

from .colors import colors
from .plan import Plan
from .diff import difftext
from .run import run


class FilePlan(Plan):
    def path(self):
        return Path(os.path.join(self.root, self.name.lstrip('/')))

    def content(self):
        return self['content']

    async def diff(self):
        self.path = self.path()
        if os.path.exists(self.path):
            current_file = self.path
            with open(self.path, 'r') as f:
                current_content = f.read()
        else:
            current_file = '/dev/null'
            current_content = ''
        content = self.content()
        return difftext(
            from_file=current_file,
            to_file=self.path,
            to_content=current_content.split('\n'),
            from_content=content.split('\n'),
        )

    async def write(self):
        diff = await self.diff()
        if diff:
            dirname = os.path.dirname(self.path)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            with open(self.path, 'w') as f:
                f.write(self.content())

        if 'mode' in self:
            await run(f'chmod {self["mode"]} {self.path}')

        if 'owner' in self:
            await run(f'chown {self["owner"]} {self.path}')

        if 'group' in self:
            await run(f'chgrp {self["group"]} {self.path}')

        print(''.join([
            colors['greenbold'],
            '✔ ',
            colors['reset'],
            colors.color(251),
            str(self.path),
            colors['reset'],
        ]))
        return diff

    async def destroy(self):
        self.path = self.path()
        if self.path.exists():
            self.path.unlink()
