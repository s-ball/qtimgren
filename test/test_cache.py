#  SPDX-FileCopyrightText: 2025-present s-ball <s-ball@laposte.net>
#  #
#  SPDX-License-Identifier: MIT
import fnmatch
import os.path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from PySide6.QtWidgets import QApplication

import qtimgren.abstract_view
from qtimgren.profile_manager import Profile


class TestDB(unittest.TestCase):
    def test_threadsafe(self):
        import sqlite3

        con = sqlite3.connect(":memory:")
        data = con.execute("""
            select * from pragma_compile_options
            where compile_options like 'THREADSAFE=%'
        """).fetchall()
        self.assertIn(('THREADSAFE=1',), data)


class TestCache(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance()
        if not cls.app:
            cls.app = QApplication()

    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        data = os.path.join(os.path.dirname(__file__), 'data')
        shutil.copytree(data, self.folder.name, dirs_exist_ok=True)
        os.remove(os.path.join(self.folder.name, 'qtimgren.sqlite'))
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
            if i.is_file() and fnmatch.fnmatch(i.name, '*.jpg') and n > 0:
                n -= 1
                self.model.cache.get_thumbnail(i.name)
        # noinspection PyUnresolvedReferences
        self.assertEqual(8, self.model.cache.con.cursor().execute(
            "SELECT COUNT(*) FROM thumbnails WHERE name like 'DSC%'").fetchone()[0])

    def test_inserted(self):
        n = 8
        thumbnails = {}
        for i in os.scandir(self.folder.name):
            if i.is_file() and fnmatch.fnmatch(i.name, '*.jpg') and n > 0:
                n -= 1
                thumbnails[i.name] = self.model.cache.get_thumbnail(i.name)
        with patch('PySide6.QtGui.QImage.scaled') as scaled:
            for file, data in thumbnails.items():
                self.assertEqual(data, self.model.cache.get_thumbnail(file))
            scaled.assert_not_called()

    def load_cache(self):
        thumbnails = {}
        for i in os.scandir(self.folder.name):
            if i.is_file() and fnmatch.fnmatch(i.name, '*.jpg'):
                thumbnails[i.name] = self.model.cache.get_thumbnail(i.name)

    def test_clean(self):
        self.load_cache()
        files = [i.name for i in os.scandir(self.folder.name) if fnmatch.fnmatch(i.name, 'DSC*')]
        self.assertEqual(8, self.model.cache.clean(files))

    def test_prune(self):
        self.load_cache()
        self.assertEqual(16, self.model.cache.prune())


if __name__ == '__main__':
    unittest.main()
