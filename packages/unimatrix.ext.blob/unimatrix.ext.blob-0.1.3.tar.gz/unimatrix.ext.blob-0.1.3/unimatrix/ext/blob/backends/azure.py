"""Declares :class:`AzureStorageBackend`."""
import contextlib
import os

try:
    from azure.core.exceptions import ResourceNotFoundError
    from azure.identity.aio import DefaultAzureCredential
    from azure.storage.blob.aio import BlobClient
    INSTALLED = True
except ImportError: # pragma: no cover
    INSTALLED = False
import aiofiles

from .base import BaseStorageBackend


class AzureStorageBackend(BaseStorageBackend):
    """A :class:`BaseStorageBackend` implementation that uses Microsoft Azure
    Blob Storage as the underlying storage provider.

    It is recommended to set a storage retention policy on the storage container
    used with :class:`AzureStorageBackend`. The implementation relies on
    soft deletes being available (i.e. ``BlobClient.undelete_blob()``).
    """
    __module__ = 'unimatrix.ext.blob'
    default_base_path: str = ''
    absolute_base_path: bool = False

    #: The URL of the Microsoft Azure storage account
    account_url: str = None

    def __init__(self,
        account: str,
        container: str,
        base_path: str = None
    ):
        """Initialize a new :class:`AzureStorageBackend` instance."""
        if not INSTALLED: # pragma: no cover
            raise ImportError(
                "Either Module azure-storage-blob or azure-identity is not "
                "installed. Please run pip install azure_storage_blob "
                "azure-identity to use the unimatrix.ext.octet module with "
                "Microsoft Azure."
            )
        super().__init__(base_path)
        self.account_url = f'https://{account}.blob.core.windows.net'
        self.container = container
        self.credential = None

    async def download(self, src: str, dst: str):
        """Downloads file from *absolute path* `src` to `dst` on the local
        filesystem.
        """
        async with self.get_blob_client(src) as blob:
            downloader = await blob.download_blob()
            async with aiofiles.open(dst, 'wb') as f:
                async for chunk in downloader.chunks():
                    await f.write(chunk)

    async def exists_internal(self, path: str) -> bool:
        """Test whether an absolute path exists.  Returns False for broken
        symbolic links if the storage backend supports them.
        """
        async with self.get_blob_client(path) as blob:
            return await blob.exists()

    async def upload(self, src: str, dst: str):
        """Uploads absolute path `src` to absolute path `dst`."""
        if not os.path.exists(src) or not os.path.isfile(src): # pragma: no cover
            raise FileNotFoundError(f"No such file: {src}")
        async with self.get_blob_client(dst) as blob:
            is_new = await blob.exists()
            must_undelete = False
            if not is_new:
                try:
                    await blob.delete_blob()
                    must_undelete = True # pragma: no cover
                except ResourceNotFoundError:
                    pass
            try:
                await blob.create_append_blob()
                async with aiofiles.open(src, 'rb') as f:
                    while True:
                        buf = await f.read(self.upload_chunk_size)
                        if not buf:
                            break
                        await blob.append_block(buf)
            except Exception: # pragma: no cover pylint: disable=W0703
                if must_undelete:
                    await blob.undelete_blob()
                raise

    @contextlib.asynccontextmanager
    async def get_blob_client(self, path: str):
        """Return a :class:`azure.storage.blob.aio.BlobClient` instance
        configured for the given `path`.
        """
        params = {
            'blob_name': path,
            'container_name': self.container
        }
        try:
            client = self._client_factory(BlobClient,
                account_url=self.account_url, **params
            )
            yield client
        finally:
            await client.close()
            if client.credential != self.credential:
                await client.credential.close()

    def _client_factory(self, cls, *args, **kwargs): # pragma: no cover
        return cls(
            credential=self.credential or DefaultAzureCredential(),
            *args, **kwargs
        )

    async def __aenter__(self):
        if self.credential is not None:
            raise TypeError("AzureStorageBackend.credential must be None")
        self.credential = DefaultAzureCredential()
        return self

    async def __aexit__(self, cls, exc, tb):
        await self.credential.close()
        self.credential = None
        return
