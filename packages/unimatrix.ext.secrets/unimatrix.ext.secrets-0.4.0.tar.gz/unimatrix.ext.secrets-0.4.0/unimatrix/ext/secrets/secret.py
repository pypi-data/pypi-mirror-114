"""Declares :class:`Secret`."""
import logging
from collections import defaultdict

import yaml
from unimatrix.lib.datastructures import ImmutableDTO

from . import providers


NOT_LOADED = object()


class Secret:
    """Represents a secret value stored in a secret storage backend, such
    as Azure Key Vault or Google Secret Manager.
    """
    __module__ = 'unimatrix.ext.secrets'
    logger = logging.getLogger('unimatrix.ext.secrets')

    @property
    def alias(self) -> str:
        return self.__alias

    @property
    def content_type(self):
        return self.__content_type

    @property
    def encoding(self) -> str:
        return self.__encoding

    @property
    def name(self) -> str:
        return self.__name

    @property
    def opts(self) -> ImmutableDTO:
        return self.__opts

    @property
    def provider(self) -> str:
        return self.__provider

    def __init__(self,
        provider: str,
        name: str,
        opts: dict,
        alias: str = None,
        encoding: str = None,
        content_type=None
    ):
        """Initializes a new secret."""
        self.__provider = provider
        self.__name = name
        self.__opts = ImmutableDTO.fromdict(opts)
        self.__alias = alias
        self.__encoding = encoding
        self.__versions = defaultdict(lambda: NOT_LOADED)
        self.__content_type = content_type

    async def get(self, version: str):
        """Asynchronously retrieve the secret content from its storage
        backend.
        """
        v = self.__versions[version]
        if v == NOT_LOADED:
            self.__versions[version] =\
                self._encode(await providers.get(self, version))
            self.logger.debug(
                "Imported secret (provider: %s, name: %s, alias: %s)",
                self.provider, self.name, self.alias or self.name
            )
        return self.__versions[version]

    def __getitem__(self, version):
        v = self.__versions[version]
        if v == NOT_LOADED:
            v = providers.get_sync(self, version)
            self.__versions[version] = self._encode(v)
            self.logger.debug(
                "Imported secret (provider: %s, name: %s, alias: %s)",
                self.provider, self.name, self.alias or self.name
            )
        return self.__versions[version]

    def _encode(self, value):
        if self.content_type in ("application/json", "application/yaml"):
            value = ImmutableDTO(yaml.safe_load(bytes.decode(value, 'utf-8')))
        elif self.__encoding and not isinstance(value, str):
            value = bytes.decode(value, self.__encoding)
        return value

    def __repr__(self):
        return f'<Secret: {self.__name}>'
