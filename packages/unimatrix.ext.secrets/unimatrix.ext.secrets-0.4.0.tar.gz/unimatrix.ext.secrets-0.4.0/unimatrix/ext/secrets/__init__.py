# pylint: skip-file
from .conf import load
from .registry import registry


__all__ = [
    'add',
    'get',
    'get_sync',
    'load',
]


def add(params):
    """Adds a new secret to the secret registry."""
    registry.add(params)


def get_sync(name, version=None):
    """Retrieve a secret from the registry. Optionally
    `version` may be specified to indicate a version. If
    the `version` argument is omitted, then the latest
    version is returned.
    """
    return registry[name][version]


async def get(name, version=None):
    """Retrieve a secret from the registry. Optionally
    `version` may be specified to indicate a version. If
    the `version` argument is omitted, then the latest
    version is returned.
    """
    return await registry.get(name, version)
