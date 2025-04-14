#  SPDX-FileCopyrightText: 2025-present s-ball <s-ball@laposte.net>
#  #
#  SPDX-License-Identifier: MIT
import fnmatch
import glob
import os.path
import shutil
import tempfile
import unittest
from unittest.mock import patch

import PySide6.QtGui
from PySide6.QtGui import QGuiApplication

import qtimgren.abstract_view
from qtimgren.profile_manager import Profile


class TestCache(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QGuiApplication()

    @classmethod
    def tearDownClass(cls):
        del cls.app

    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        data = os.path.join(os.path.dirname(__file__), 'data')
        shutil.copytree(data, self.folder.name, dirs_exist_ok=True)
        self.profile = Profile('data', self.folder.name)
        self.model = qtimgren.abstract_view.Model(self.profile)

    def tearDown(self):
        self.model.cache.close()
        self.folder.cleanup()

    def test_copy_ok(self):
        nb_files = len(os.listdir(self.model.folder))
        self.assertEqual(18, nb_files)

    def test_insert(self):
        n = 8
        for i in os.scandir(self.folder.name):
            if i.is_file() and fnmatch.fnmatch(i.name, '*.jpg') and n>0:
                n -= 1
                self.model.cache.get_thumbnail(i.name)
        self.assertEqual(8, self.model.cache.con.cursor().execute(
            "SELECT COUNT(*) FROM thumbnails WHERE name like 'DSC%'"
        ).fetchone()[0])

    def test_inserted(self):
        n = 8
        thumbnails = {}
        for i in os.scandir(self.folder.name):
            if i.is_file() and fnmatch.fnmatch(i.name, '*.jpg') and n>0:
                n -= 1
                thumbnails[i.name] = self.model.cache.get_thumbnail(i.name)
        with patch('PySide6.QtGui.QImage.scaled') as scaled:
            for file, data in thumbnails.items():
                self.assertEqual(data, self.model.cache.get_thumbnail(file))
            scaled.assert_not_called()

if __name__ == '__main__':
    unittest.main()
