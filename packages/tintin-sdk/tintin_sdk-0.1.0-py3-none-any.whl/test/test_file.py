import unittest

from tintin.file.http import FileManager as httpFileManager
from tintin.file.minio import FileManager as minioFileManager

from .file import (ParametrizedTestCase, FileManagerTestCase)

class TestFileManagerLauncher(unittest.TestCase):
    def suite(self):
        suite = unittest.TestSuite()
        suite.addTest(ParametrizedTestCase.parametrize(FileManagerTestCase, httpFileManager))
        suite.addTest(ParametrizedTestCase.parametrize(FileManagerTestCase, minioFileManager))
        return suite

    def test_all(self):
        runner = unittest.TextTestRunner()
        runner.run(self.suite())

if __name__ == '__main__':
    unittest.main()
