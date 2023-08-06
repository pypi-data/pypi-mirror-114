"""Declares :class:`Provider`."""
import abc


class Provider(metaclass=abc.ABCMeta):
    """The base class for all provider implementations."""
    __module__ = 'unimatrix.ext.secrets.providers'

    @abc.abstractmethod
    def get_secret_version_sync(self, secret: 'Secret', version: str = None):
        """Return a version for the given :class:`Secret` object."""
        raise NotImplementedError

    @abc.abstractmethod
    async def get_secret_version(self, secret: 'Secret', version: str = None):
        """Return a version for the given :class:`Secret` object."""
        raise NotImplementedError
