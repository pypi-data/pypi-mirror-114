"""Declares :class:`Registry`."""
import logging
from collections import defaultdict

from .secret import Secret


class Registry:
    """Provides an interface to store secret in the local
    memory, and to lookup.
    """
    __module__ = 'unimatrix.ext.secrets'
    logger = logging.getLogger('unimatrix.ext.secrets')

    def __init__(self):
        self.__secrets = {}

    def add(self, params):
        """Add a secret to the registry."""
        secret = Secret(**params)
        self.__secrets[secret.alias or secret.name] = secret
        self.logger.debug(
            "Configured secret (provider: %s, name: %s, alias: %s)",
            secret.provider, secret.name, secret.alias or secret.name
        )

    async def get(self, name: str, version: str):
        """Asynchronously retrieve the secret content from its storage
        backend.
        """
        return await self.__secrets[name].get(version)

    def __getitem__(self, name):
        return self.__secrets[name]


registry = Registry()
