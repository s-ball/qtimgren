# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""


from PySide2.QtCore import Slot,  Qt
from PySide2.QtWidgets import QMainWindow,  QApplication,  QMenu, QWidget

from .ui_main_window import Ui_MainWindow
from .about import About
from .profile import ProfileDialog
from .profiles import ProfilesDialog
from .profile_manager import ProfileManager
from typing import Optional


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Main window for QtImgren.
    """
    def __init__(self, parent: Optional[QWidget] = None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        profile_menu = self.findChild(QMenu,  "menu_Profiles")
        self.profile_manager = ProfileManager(profile_menu,  self)
    
    @Slot()
    def on_action_About_triggered(self):
        """
        Displays About dialog.
        """
        about = About()
        about.setWindowFlag(Qt.WindowContextHelpButtonHint,  False)
        about.exec_()
    
    @Slot()
    def on_actionAbout_Qt_triggered(self):
        """
        Displays About Qt dialog.
        """
        QApplication.aboutQt()

    @Slot()
    def on_action_New_profile_triggered(self):
        """
        Create a new profile.
        """
        profile = ProfileDialog(self,  names=self.profile_manager.names())
        cr = profile.exec_()
        if cr:
            self.profile_manager.add_from_dialog(profile)
    
    @Slot()
    def on_action_Manage_profiles_triggered(self):
        """
        Manage (edit or remove) existing profiles.
        """
        dialog = ProfilesDialog(self.profile_manager.profiles,  self)
        cr = dialog.exec_()
        if cr:
            self.profile_manager.reset_profiles(dialog.model.profiles)
