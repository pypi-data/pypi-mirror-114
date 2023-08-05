import difflib
import pathlib
import os

from .colors import colors


def difftext(from_file, to_file, from_content, to_content):
    result = []
    for line in difflib.unified_diff(to_content, from_content):
        result.append(line)
    if result:
        result[0] = f'--- {from_file}'
        result[1] = f'+++ {to_file}'
    if not result:
        return ''

    colored = []
    for line in result:
        if line.startswith('+'):
            colored.append(
                colors['green'] + line + colors['reset']
            )
        elif line.startswith('-'):
            colored.append(
                colors['red'] + line + colors['reset']
            )
        else:
            colored.append(line)
    return '\n'.join(colored)


class Plan(dict):
    def __init__(self, config, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.config = config

    async def write(self, root):
        pass

    async def activate(self, root):
        pass

    async def diff(self, root):
        pass

    async def destroy(self, root):
        pass


class FilePlan(Plan):
    def path(self, root):
        return pathlib.Path(os.path.join(root, f'{self.name}.{self.ext}'))

    async def diff(self, root):
        self.path = self.path(root)
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

    async def write(self, root):
        diff = await self.diff(root)
        if diff:
            dirname = os.path.dirname(self.path)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            with open(self.path, 'w') as f:
                f.write(self.content())
        print(''.join([
            colors['greenbold'],
            '✔ ',
            colors['reset'],
            colors.color(251),
            str(self.path),
            colors['reset'],
        ]))
        return diff

    async def destroy(self, root):
        self.path = self.path(root)
        if self.path.exists():
            self.path.unlink()
