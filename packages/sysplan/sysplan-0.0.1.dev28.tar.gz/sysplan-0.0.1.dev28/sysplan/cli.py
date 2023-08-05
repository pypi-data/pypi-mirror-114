"""
Apply plans parsed from /etc/sysplan.d/*.yaml.
"""

import asyncio
import contextvars
import cli2

from .config import Config, SYSPLAN_D, SYSPLAN_ROOT


cli = cli2.Group(doc=__doc__)

context = contextvars.ContextVar('context')


@cli.cmd(color='green')
async def diff(*plans):
    """
    Show diff without applying /etc/sysplan.d/*.yaml.
    """
    for config in Config.factory(SYSPLAN_D):
        for plan in config.plans(SYSPLAN_ROOT, *plans):
            output = await plan.diff()
            if output:
                print(output)


@cli.cmd
async def apply(*plans):
    """
    Apply plans parsed from /etc/sysplan.d/*.yaml.
    """
    await write(*plans)
    await activate(*plans)


@cli.cmd
async def write(*plans):
    """
    Write configuration for plans.
    """
    for config in Config.factory(SYSPLAN_D):
        for plan in config.plans(SYSPLAN_ROOT, *plans):
            diff = await plan.write()
            if diff:
                print(diff)


@cli.cmd
async def activate(*plans):
    """
    Write configuration for plans.
    """
    for config in Config.factory(SYSPLAN_D):
        await asyncio.gather(*[
            plan.activate()
            for plan in config.plans(SYSPLAN_ROOT, *plans)
        ])


@cli.cmd(color='red')
async def destroy(*plans):
    """
    Stop, disable, destroy plans.
    """
    for config in Config.factory(SYSPLAN_D):
        await asyncio.gather(*[
            plan.destroy()
            for plan in config.plans(SYSPLAN_ROOT, *plans)
        ])


if __name__ == '__main__':
    cli.entry_point()
