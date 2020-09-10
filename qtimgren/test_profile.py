import unittest
import qtimgren.profile
from PySide2.QtWidgets import *
from PySide2.QtCore import Qt
from qtimgren.main_window import MainWindow
from qtimgren.profile_manager import Profile
from unittest.mock import patch


class TestProfile(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app = QApplication.instance()
        if cls.app is None:
            cls.app = QApplication()

    @classmethod
    def tearDownClass(cls) -> None:
        del cls.app

    def setUp(self) -> None:
        self.main = MainWindow()
        self.main.show()

    def tearDown(self) -> None:
        self.main.close()

    def test_new(self):
        names = ('a', 'b')
        dialog = qtimgren.profile.ProfileDialog(self.main, names=names)
        self.assertEqual(names, dialog.names)
        name = dialog.findChild(QLineEdit, 'name')
        self.assertEqual('', name.text())

    def test_edit(self):
        profile = Profile('a', 'b', 'c', True)
        dialog = qtimgren.profile.ProfileDialog(self.main, profile)
        self.assertEqual(0, len(dialog.names))
        name = dialog.findChild(QLineEdit, 'name')
        self.assertEqual('a', name.text())
        recurse = dialog.findChild(QCheckBox, 'recurse')
        self.assertEqual(Qt.Checked, recurse.checkState())

    def test_valid_name_empty(self):
        names = ('a', 'b')
        dialog = qtimgren.profile.ProfileDialog(self.main, names=names)
        with patch.object(qtimgren.profile, 'QMessageBox') as msg_box:
            self.assertFalse(dialog.valid())
            self.assertEqual(1, msg_box.warning.call_count)

    def test_valid_name_used(self):
        names = ('a', 'b')
        dialog = qtimgren.profile.ProfileDialog(self.main, names=names)
        with patch.object(qtimgren.profile, 'QMessageBox') as msg_box:
            child = dialog.findChild(QLineEdit, 'name')
            child.setText('a')
            self.assertFalse(dialog.valid())
            self.assertEqual(1, msg_box.warning.call_count)

    def test_valid_path_wrong(self):
        names = ('a', 'b')
        dialog = qtimgren.profile.ProfileDialog(self.main, names=names)
        with patch.object(qtimgren.profile, 'QMessageBox') as msg_box:
            name = dialog.findChild(QLineEdit, 'name')
            name.setText('c')
            child = dialog.findChild(QLineEdit, 'path')
            child.setText(__file__)
            self.assertFalse(dialog.valid())
            self.assertEqual(1, msg_box.warning.call_count)

    def test_valid_mask_wrong(self):
        names = ('a', 'b')
        dialog = qtimgren.profile.ProfileDialog(self.main, names=names)
        with patch.object(qtimgren.profile, 'QMessageBox') as msg_box:
            name = dialog.findChild(QLineEdit, 'name')
            name.setText('c')
            path = dialog.findChild(QLineEdit, 'path')
            path.setText('.')
            child = dialog.findChild(QLineEdit, 'mask')
            child.setText('foo')
            self.assertFalse(dialog.valid())
            self.assertEqual(1, msg_box.warning.call_count)


if __name__ == '__main__':
    unittest.main()
