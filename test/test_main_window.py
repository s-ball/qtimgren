import unittest
from PySide2.QtWidgets import *
from qtimgren.main_window import MainWindow
from unittest.mock import Mock, patch
import qtimgren.main_window
import qtimgren.about
import qtimgren.profile
import qtimgren.profiles


class TestMainWindow(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app = QApplication.instance()
        if cls.app is None:
            cls.app = QApplication()

    def setUp(self) -> None:
        self.window = MainWindow()
        self.window.show()

    def tearDown(self) -> None:
        self.window.close()

    def test_about(self):
        about = Mock(qtimgren.about.About)
        about.exec_ = Mock()
        about.exec = about.exec_
        with patch.object(qtimgren.main_window, 'About') as About:
            About.return_value = about
            action = self.window.findChild(QAction, 'action_About')
            action.triggered.emit()
            about.exec_.assert_called_once_with()

    def test_about_qt(self):
        with patch.object(qtimgren.main_window, 'QApplication') as qApp:
            action = self.window.findChild(QAction, 'actionAbout_Qt')
            action.triggered.emit()
            qApp.aboutQt.assert_called_once_with()

    def test_close(self):
        self.assertTrue(self.window.isVisible())
        action = self.window.findChild(QAction, 'action_Quit')
        action.triggered.emit()
        self.assertFalse(self.window.isVisible())

    def test_new_profile(self):
        dialog = Mock(qtimgren.profile.ProfileDialog)
        with patch.object(self.window, 'profile_manager') as pm, \
                patch.object(qtimgren.main_window, 'ProfileDialog') as Dialog:
            pm.names.return_value = ['a', 'b']
            Dialog.return_value = dialog
            dialog.exec_ = Mock()
            dialog.exec = dialog.exec_
            dialog.exec_.return_value = 1
            action = self.window.findChild(QAction, 'action_New_profile')
            action.triggered.emit()
            Dialog.assert_called_once_with(self.window, names=['a', 'b'])
            dialog.exec_.assert_called_once_with()
            pm.add_from_dialog.assert_called_once_with(dialog)

    def test_manage_profiles(self):
        dialog = Mock(qtimgren.profiles.ProfilesDialog)
        with patch.object(self.window, 'profile_manager') as pm, \
                patch.object(qtimgren.main_window, 'ProfilesDialog') as Dialog:
            Dialog.return_value = dialog
            dialog.exec_.return_value = 1
            dialog.model = Mock()
            dialog.exec = Mock()
            dialog.exec_ = dialog.exec
            action = self.window.findChild(QAction, 'action_Manage_profiles')
            action.triggered.emit()
            Dialog.assert_called_once_with(pm.profiles, self.window)
            dialog.exec.assert_called_once_with()
            pm.reset_profiles.assert_called_once_with(dialog.model.profiles)


if __name__ == '__main__':
    unittest.main()
