# pylint: skip-file
import os
import tempfile
import unittest

from .. import local


class LocalDiskBackendUnitTestCase(unittest.TestCase):

    def test_constructor_sets_cwd_when_base_path_is_none(self):
        backend = local.LocalDiskBackend()
        self.assertEqual(backend.base_path, os.getcwd())

    def test_constructor_sets_base_path_to_current_cwd(self):
        cwd = os.getcwd()
        try:
            os.chdir(tempfile.gettempdir())
            backend = local.LocalDiskBackend()
        finally:
            os.chdir(cwd)
        self.assertNotEqual(backend.base_path, cwd)

    def test_constructor_creates_base_path_if_relative(self):
        cwd = os.getcwd()
        dirname = bytes.hex(os.urandom(16))
        try:
            os.chdir(tempfile.gettempdir())
            backend = local.LocalDiskBackend(base_path=dirname)
        finally:
            os.chdir(cwd)
        self.assertTrue(os.path.exists(
            os.path.join(tempfile.gettempdir(), dirname)
        ))
