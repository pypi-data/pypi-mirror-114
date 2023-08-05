"""Simple buvar staging.

Invoke via :code:`python -m buvar -m buvar_aiohttp.static`
"""
import asyncio
import importlib.util
import typing as t

import attr
import structlog

from buvar import Components, config, fork, log

sl = structlog.get_logger()


@attr.s(auto_attribs=True, kw_only=True)
class BuvarConfig(config.Config, section="buvar"):
    log_level: str = "info"
    forks: int = 1
    plugins: t.Sequence[str] = attr.ib(factory=list)
    sockets: t.Sequence[str] = attr.ib(factory=list)
    show_warnings: bool = config.bool_var(False)


def find_loop_specs():
    """Just find specs for common loops."""
    module_specs = (
        (module_name, importlib.util.find_spec(module_name))
        for module_name in ("uvloop", "asyncio")
    )
    available_specs = {
        module_name: spec for module_name, spec in module_specs if spec is not None
    }
    return available_specs


available_loops = find_loop_specs()


def set_loop_policy(event_loop=None):
    loop_module = next(
        (
            spec.loader.load_module()
            for module, spec in available_loops.items()
            if event_loop is None or module == event_loop
        ),
        None,
    )
    if loop_module is not None and loop_module is not asyncio:
        asyncio.set_event_loop_policy(loop_module.EventLoopPolicy())
        sl.info("Event loop policy", policy=loop_module.EventLoopPolicy)


components = Components()

source = components.add(config.ConfigSource(env_prefix="BUVAR"))
buvar_config = source.load(BuvarConfig)

log_config = log.LogConfig(level=buvar_config.log_level)
log_config.setup()

set_loop_policy("uvloop")

fork.stage(
    *buvar_config.plugins,
    components=components,
    forks=buvar_config.forks,
    sockets=buvar_config.sockets,
)
