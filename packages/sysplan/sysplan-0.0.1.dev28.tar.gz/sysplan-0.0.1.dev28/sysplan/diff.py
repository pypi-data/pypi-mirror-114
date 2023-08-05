import difflib

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
