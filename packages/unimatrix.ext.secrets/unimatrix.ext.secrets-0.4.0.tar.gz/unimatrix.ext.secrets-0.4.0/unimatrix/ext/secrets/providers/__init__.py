# pylint: skip-file
import ioc.loader


__all__ = [
    'get_provider',
    'get_sync'
]


PROVIDER_CLASSES = {
    'azure': 'unimatrix.ext.secrets.providers.azure.AzureProvider',
    'google': 'unimatrix.ext.secrets.providers.google.GoogleProvider'
}


def get_provider(kind):
    """Return a :class:`~unimatrix.ext.crypto.providers.Provider` instance
    of the given `kind`.
    """
    return ioc.loader.import_symbol(PROVIDER_CLASSES[kind])()


def get_sync(secret, version=None):
    """Resolve the provider for `secret` :class:`~unimatrix.ext.secrets.Secret`
    and return secret content.
    """
    return get_provider(secret.provider)\
        .get_secret_version_sync(secret, version)


async def get(secret, version=None):
    """Resolve the provider for `secret` :class:`~unimatrix.ext.secrets.Secret`
    and return secret content.
    """
    return await get_provider(secret.provider)\
        .get_secret_version(secret, version)
