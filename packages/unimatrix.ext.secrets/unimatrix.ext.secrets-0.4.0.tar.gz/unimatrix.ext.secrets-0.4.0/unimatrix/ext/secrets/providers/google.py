"""Declares :class:`GoogleProvider`."""
from google.cloud import secretmanager

from .base import Provider


class GoogleProvider(Provider):
    """Secret storage implementation for Google Secret Manager."""
    client = secretmanager.SecretManagerServiceAsyncClient()
    client_sync = secretmanager.SecretManagerServiceClient()

    def get_secret_version_sync(self, secret: 'Secret', version: str) -> bytes:
        response = self.client_sync.access_secret_version(
            name=self.client_sync.secret_version_path(
                secret.opts.project, secret.name, version or 'latest')
        )
        return response.payload.data

    async def get_secret_version(self, secret: 'Secret', version: str =None):
        response = await self.client.access_secret_version(
            name=self.client.secret_version_path(
                secret.opts.project, secret.name, version or 'latest')
        )
        return response.payload.data
