import tempfile
import io
import os
import unittest
from unittest import mock

from tintin.util import list_all_files

debug = False
host = 'https://api.tintin.footprint-ai.com'
project_id = '1vpe4zw1y68gnj308j7xol0krd3529'
m = mock.patch.dict(os.environ, {
    'TINTIN_SESSION_TEMPLATE_PROJECT_ID': project_id,
    'TINTIN_SESSION_TEMPLATE_PROJECT_TOKEN_MINIO_DOWNLOAD': 'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiIqLmZvb3RwcmludC1haS5jb20iLCJleHAiOjIyNTc3ODA4ODgsImp0aSI6IjQ0ODkxNDVlLTAzZWEtNDA2Yy1iZTFmLWViMWUxNjcxNmJlOCIsImlhdCI6MTYyNzA2MDg4OCwiaXNzIjoiYXV0aG9yaXphdGlvbi5mb290cHJpbnQtYWkuY29tIiwibmJmIjoxNjI3MDYwODg4fQ.uMRPw5JIW9O35MqsPhLJ2FR-fzx7IadRz51cVmeX_f94O3900M8r2B4ikcCdoDAXQpsTvfZpj88gBewtoOdz_Q',
    'TINTIN_SESSION_TEMPLATE_MINIO_ACCESS_KEY': '1vpe4zw1y68gnj308j7xol0krd3529',
    'TINTIN_SESSION_TEMPLATE_MINIO_SECRET_KEY': '25aa64a5-3fb9-48ad-a05c-203b177061c0',
    'TINTIN_SESSION_TEMPLATE_MINIO_BUCKET': '1vpe4zw1y68gnj308j7xol0krd3529',
    'TINTIN_SESSION_TEMPLATE_MINIO_ENDPOINT': 'minio-ec.tintin.svc.cluster.local:9000'
})

class ParametrizedTestCase(unittest.TestCase):
    """ TestCase classes that want to be parametrized should
        inherit from this class.
    """
    def __init__(self, methodName='runTest', fileManagerMaker=None):
        print('ParametrizedTestCase is called,', fileManagerMaker)
        super(ParametrizedTestCase, self).__init__(methodName)
        self.fileManagerMaker= fileManagerMaker

    @staticmethod
    def parametrize(testcase_klass, fileManagerMaker):
        """ Create a suite containing all tests taken from the given
            subclass, passing them the parameter 'param'.
        """
        print('ParametrizedTestCase.parametrize called, ', testcase_klass, ' m:', fileManagerMaker)
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testcase_klass)
        suite = unittest.TestSuite()
        for name in testnames:
            print('testname:', name)
            suite.addTest(testcase_klass(name, fileManagerMaker))
        return suite

class FileManagerTestCase(ParametrizedTestCase):
    global m
    global host
    global debug

    def setUp(self):
        m.start()
        self.fileManagerUnderTest = self.fileManagerMaker(host, debug)

    def tearDown(self):
        m.stop()

    def test_1_folder_upload(self):
        # should upload to destination with /testupload/testdata/...
        self.assertEqual(self.fileManagerUnderTest.upload('/testupload', './testdata'), True)

    def test_2_file_upload(self):
        # should upload to destination /testupload/testdata/1.txt individual file
        self.assertEqual(self.fileManagerUnderTest.upload('/testupload', './testdata/1.txt'), True)

    #def test_3_http_file_download(self):
    #    with tempfile.TemporaryDirectory() as tmpdirname:
    #        self.assertEqual(self.fileManagerUnderTest.download(tmpdirname,
    #            ['https://api.tintin.footprint-ai.com/api/v1/project/{}/minio/object/testupload/testdata/1.txt'.format(project_id)],
    #        ), True)
    #        self.assertEqual(1, len(list_all_files(tmpdirname)))

    def test_4_localpath_file_download(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            self.assertEqual(self.fileManagerUnderTest.download(tmpdirname,
                ['/testupload/testdata/1.txt'],
            ), True)
            self.assertEqual(1, len(list_all_files(tmpdirname)))

    def test_5_localpath_download_notfound(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            self.assertEqual(self.fileManagerUnderTest.download(tmpdirname,
                ['/testupload/testdata/notfound.jpg'],
            ), False)
            self.assertEqual(0, len(list_all_files(tmpdirname)))

    def test_6_localpath_dir_download(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            self.assertEqual(self.fileManagerUnderTest.download(tmpdirname,
                ['/testupload/testdata'],
                True,
            ), True)
            self.assertEqual(3, len(list_all_files(tmpdirname)))
            # [1.txt, 2.txt, dir1/f1.txt]
