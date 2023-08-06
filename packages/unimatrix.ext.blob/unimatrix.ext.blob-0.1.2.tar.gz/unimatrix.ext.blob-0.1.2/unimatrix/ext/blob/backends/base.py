"""Declares :class:`BaseStorageBackend`."""
import io
import os
import pathlib
import tempfile

import aiofiles

from .istoragebackend import IStorageBackend


class BaseStorageBackend(IStorageBackend):
    """The base class for all storage backends."""
    __module__ = 'unimatrix.ext.blob'

    #: Specifies the capabilities of the backend.
    capabilities: list = []

    #: Specifies the supported write modes by a :class:`BaseStorageBackend`
    #: implementation.
    write_modes: list = ['w', 'wt', 'wb']

    #: Specifies the supported read modes by a :class:`BaseStorageBackend`
    #: implementation.
    read_modes: list = ['r', 'rt', 'rb']

    #: Indicates the default base path for this storage backend. If this
    #: attribute is ``None``, then the ``base_path`` parameter is mandatory
    #: when creating a new instance.
    default_base_path: str = None

    #: Indicates if the backend allows absolute storage base paths.
    absolute_base_path: str = True

    @staticmethod
    async def ensure_path(source) -> str:
        """Ensure that `source` is readable from a filepath and return a
        string holding the filepath.

        The `source` parameter can be any of the following:

        - A file-like object.
        - A byte-sequence.
        - A string or :class:`pathlib.Path` instance.
        - A callable. The callable is expected to take a positional argument
          indicating the number of bytes to read. It must not block when there
          are no bytes left to read, but return an empty string or object that
          otherwise evaluates to ``False``.
        """
        if isinstance(source, (str, pathlib.Path)):
            return source
        elif hasattr(source, 'read') and hasattr(source, 'name'):
            # File-like object that has a name attribute that indicates
            # the local filepath.
            return source.name
        elif isinstance(source, (bytes, io.BytesIO)):
            _, fp = tempfile.mkstemp()
            if isinstance(source, io.BytesIO):
                source = source.read()
            async with aiofiles.open(fp, 'wb') as f:
                await f.write(source)
            return fp
        elif callable(source):
            _, fp = tempfile.mkstemp()
            async with aiofiles.open(fp, 'wb') as f:
                while True:
                    buf = source(1024)
                    if not isinstance(buf, bytes) and buf:
                        # Assume coroutine/generator here
                        buf = await buf
                    if not buf:
                        break
                    await f.write(buf)
            return fp
        else: # pragma: no cover
            raise TypeError(f"Invalid type: {type(source).__name__}")

    def __init__(self, base_path=None):
        """Initialize the storage backend.

        Args:
            base_path (str): the base path that the storage backend writes
                all files relative to. If `base_path` is ``None``, then
                :attr:`default_base_path` is used.
        """
        if base_path is None: # pragma: no cover
            self.base_path = self.default_base_path\
                if not callable(self.default_base_path)\
                else self.default_base_path()
        else:
            self.base_path = base_path
        if self.base_path is None: # pragma: no cover
            raise TypeError(
                "The `base_path` argument was not provided and "
                "no default was set for storage backend implementation"
                f" {type(self).__name__}"
            )

        if os.path.isabs(self.base_path) and not self.absolute_base_path: # pragma: no cover
            raise ValueError("Storage base path can not be absolute.")

    async def exists(self, path: str) -> bool:
        """Test whether a path exists.  Returns False for broken symbolic links
        if the storage backend supports them.
        """
        return await self.exists_internal(self.storage_path(path))

    async def pull(self, src: str, dst: str = None) -> str:
        """Pulls a file from the given `src` in the storage backend to local
        filepath `dst`. If `dst` is ``None``, then a temporary filepath is
        generated.
        """
        if dst is None:
            _, dst = tempfile.mkstemp()
        await self.download(self.storage_path(src), dst)
        return dst

    async def push(self, src: object, dst: str):
        """Copies local `src` to remote `dst`.The `src` argument is either
        a string pointing to filepath on the local filesystem, a byte-sequence
        holding the contents of the source file, or a file-like object (open
        for reading).
        """
        await self.upload(
            await self.ensure_path(src),
            self.storage_path(dst)
        )

    #def open(self, path: str, mode='rt', *args, **kwargs): # pylint: disable=W1113
    #    """Open the given `path` in the given `mode`."""
    #    if mode not in set(self.write_modes + self.read_modes): # pragma: no cover
    #        raise NotImplementedError(f"Unsupported mode: {mode}")
    #    return self.descriptor_class(self, path, mode, *args, **kwargs)

    def storage_path(self, *components):
        """Returns the absolute path in the storage of `path`."""
        return os.path.join(self.base_path or '', *components)

    async def __aenter__(self):
        return self

    async def __aexit__(self, cls, exc, tb):
        return
