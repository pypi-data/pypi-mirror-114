"""Declares :class:`AzureProvider`."""
from azure.identity.aio import DefaultAzureCredential\
    as AsyncDefaultAzureCredential
from azure.keyvault.secrets.aio import SecretClient\
    as AsyncSecretClient
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

from .base import Provider


class AzureProvider(Provider):
    """Secret storage implementation for Azure Key Vault."""
    credential_sync: DefaultAzureCredential = DefaultAzureCredential()
    clients_sync: dict = {}

    def get_sync_client(self, secret):
        """Return a synchronous Azure Key Vault client for the given
        vault.
        """
        vault = secret.opts.vault
        url = f"https://{vault}.vault.azure.net"
        if vault not in self.clients_sync:
            self.clients_sync[vault] = SecretClient(
                vault_url=url,
                credential=self.credential_sync
            )
        return self.clients_sync[vault]

    def get_secret_version_sync(self, secret: 'Secret', version: str =None):
        client = self.get_sync_client(secret)
        secret = client.get_secret(secret.name)
        return secret.value

    async def get_secret_version(self, secret: 'Secret', version: str =None):
        vault = secret.opts.vault
        url = f"https://{vault}.vault.azure.net"
        credential = AsyncDefaultAzureCredential()
        client = AsyncSecretClient(vault_url=url, credential=credential)
        async with client:
            async with credential:
                secret = await client.get_secret(secret.name)
        return secret.value
