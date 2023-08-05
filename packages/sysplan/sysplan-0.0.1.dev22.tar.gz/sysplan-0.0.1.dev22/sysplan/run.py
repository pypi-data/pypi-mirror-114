import asyncio
import os
import shlex
import sys

from .colors import colors


async def run(cmd, *args, verbose=True):
    if verbose or os.getenv('CI'):
        print(''.join([
            colors['gray2bold'],
            '+ ',
            cmd,
            colors['reset'],
        ]))

    if not args:
        args = shlex.split(cmd)

    if os.getenv('CI'):
        class ProcMock:
            def __init__(self):
                self.returncode = 0
        return ProcMock()
    else:
        proc = await asyncio.create_subprocess_exec(
            *args,
            stdout=sys.stdout if verbose else asyncio.subprocess.PIPE,
            stderr=sys.stderr if verbose else asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()

    if verbose:
        if proc.returncode != 0:
            print(
                colors["redbold"]
                + f'{cmd!r} exited with {proc.returncode}'
                + colors["reset"]
            )
        if stdout:
            print(f'{stdout.decode()}'.strip())
        if stderr:
            print(f'{stderr.decode()}'.strip())

    return proc
