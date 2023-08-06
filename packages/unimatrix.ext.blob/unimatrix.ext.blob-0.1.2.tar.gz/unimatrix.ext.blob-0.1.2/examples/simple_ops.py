# pylint: skip-file
import asyncio

from unimatrix.ext import blob


# Create a new LocalDiskBackend instance. We provide no base_path parameter
# to the constructor, so it writes relative to the current working directory.
backend = blob.LocalDiskBackend()


async def main():
    buf = b'f00'
    dst = 'my/destination/path'
    await backend.push(buf, dst)
    print( open(await backend.pull(dst)).read() )


if __name__ == '__main__':
    asyncio.run(main())
