# pylint: skip-file
import io
import tempfile
import os
import unittest

import aiofiles
import pytest


class BackendTests:
    __test__ = False
    allows_absolute_storage = False

    @pytest.fixture
    def backend(self):
        return self.get_backend()

    def get_backend(self, **kwargs):
        return self.backend_class(**self.get_backend_kwargs(**kwargs))

    def get_backend_kwargs(self, **kwargs):
        return {
            'base_path': tempfile.mkdtemp(),
            **kwargs
        }

    @pytest.mark.asyncio
    async def test_push_creates_file(self, backend):
        dst = bytes.hex(os.urandom(16))
        buf = b'foo'
        with tempfile.NamedTemporaryFile() as f:
            f.write(buf)
            f.seek(0)
            await backend.push(f.name, dst)

        assert await backend.exists(dst)

        loc = open(await backend.pull(dst), 'rb').read()
        assert buf == loc, loc

    @pytest.mark.asyncio
    async def test_push_creates_file_from_filelike(self, backend):
        dst = bytes.hex(os.urandom(16))
        buf = b'foo'
        f = io.BytesIO(buf)
        await backend.push(f, dst)
        assert await backend.exists(dst)

        loc = open(await backend.pull(dst), 'rb').read()
        assert buf == loc, loc

    @pytest.mark.asyncio
    async def test_push_creates_file_from_filelike_native(self, backend):
        dst = bytes.hex(os.urandom(16))
        _, src = tempfile.mkstemp()
        buf = b'foo'
        with open(src, 'wb+') as f:
            f.write(buf)
            f.seek(0)
            await backend.push(f, dst)
        assert await backend.exists(dst)

        loc = open(await backend.pull(dst), 'rb').read()
        assert buf == loc, loc

    @pytest.mark.asyncio
    async def test_push_creates_file_from_callable_sync(self, backend):
        dst = bytes.hex(os.urandom(16))
        buf = b'foo'
        f = io.BytesIO(buf)
        await backend.push(f.read, dst)
        assert await backend.exists(dst)

        loc = open(await backend.pull(dst), 'rb').read()
        assert buf == loc, loc

    @pytest.mark.asyncio
    async def test_push_creates_file_from_callable(self, backend):
        dst = bytes.hex(os.urandom(16))
        buf = b'foo'
        async with aiofiles.tempfile.TemporaryFile() as f:
            await f.write(buf)
            await f.seek(0)
            await backend.push(f.read, dst)
        assert await backend.exists(dst)

        loc = open(await backend.pull(dst), 'rb').read()
        assert buf == loc, loc

    @pytest.mark.asyncio
    async def test_push_creates_file_from_bytes(self, backend):
        dst = bytes.hex(os.urandom(16))
        buf = b'foo'
        await backend.push(buf, dst)
        assert await backend.exists(dst)

        loc = open(await backend.pull(dst), 'rb').read()
        assert buf == loc, loc

    @pytest.mark.asyncio
    async def test_push_creates_file_with_path(self, backend):
        dst = f'{bytes.hex(os.urandom(16))}/foo/bar/baz'
        buf = b'foo'
        with tempfile.NamedTemporaryFile() as f:
            f.write(buf)
            f.seek(0)
            await backend.push(f.name, dst)

        assert await backend.exists(dst)

    @pytest.mark.asyncio
    async def test_push_pull_is_equal(self, backend):
        dst = bytes.hex(os.urandom(16))
        buf = b'foo'
        with tempfile.NamedTemporaryFile() as f:
            f.write(buf)
            f.seek(0)
            await backend.push(f.name, dst)

        loc = open(await backend.pull(dst), 'rb').read()
        assert buf == loc, loc

    @pytest.mark.asyncio
    async def test_push_pull_is_equal_with_path(self, backend):
        dst = f'{bytes.hex(os.urandom(16))}/foo'
        buf = b'foo'
        with tempfile.NamedTemporaryFile() as f:
            f.write(buf)
            f.seek(0)
            await backend.push(f.name, dst)

        loc = open(await backend.pull(dst), 'rb').read()
        assert buf == loc, loc

    @pytest.mark.asyncio
    async def test_push_overwrite_existing(self, backend):
        dst = str(f'{bytes.hex(os.urandom(16))}/foo')
        buf = b'foo'
        await backend.push(b'bar', dst)
        await backend.push(buf, dst)

        loc = open(await backend.pull(dst), 'rb').read()
        assert buf == loc, loc

    @pytest.mark.asyncio
    async def test_ctx_push_pull_is_equal(self, backend):
        async with backend:
            dst = bytes.hex(os.urandom(16))
            buf = b'foo'
            with tempfile.NamedTemporaryFile() as f:
                f.write(buf)
                f.seek(0)
                await backend.push(f.name, dst)

            loc = open(await backend.pull(dst), 'rb').read()
            assert buf == loc, loc
