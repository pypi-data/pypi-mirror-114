# pylint: skip-file
from unimatrix.conf import settings

from .conf import load
from .registry import registry


async def on_setup(settings=settings):
    for alias, params in dict.items(getattr(settings, 'SECRETS', {})):
        registry.add({**params, 'alias': alias})

    load()


async def boot():
    pass
