# pylint: skip-file
import os
import unittest

import ioc
import pytest

from .. import azure
from .base import BackendTests


class AzureStorageBackendTestCase(BackendTests):
    __test__ = True
    backend_class = azure.AzureStorageBackend

    def get_backend_kwargs(self):
        # Check if we can authenticate with Azure.
        try:
            from azure.identity.aio import DefaultAzureCredential
            from azure.storage.blob import BlobServiceClient
        except ImportError:
            raise unittest.SkipTest()
        return {
            'account': 'unimatrixtesting',
            'container': 'unimatrix-blob'
        }

    @pytest.mark.asyncio
    async def test_context_sets_credentials(self, backend):
        assert backend.credential is None
        async with backend:
            assert backend.credential is not None
        assert backend.credential is None

    @pytest.mark.asyncio
    async def test_injected_sets_credentials(self, backend):
        backend = ioc.provide('AzureStorageBackend', backend, force=True)
        assert backend.credential is None

        @ioc.inject.context('backend', 'AzureStorageBackend')
        async def f(backend):
            assert backend.credential is not None

        await f()
        assert backend.credential is None
