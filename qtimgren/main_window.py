# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

import os

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow,  qApp,  QMenu

from .Ui_main_window import Ui_MainWindow
from .about import About
from .profile import ProfileDialog
from .profile_manager import ProfileManager

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        profile_menu = self.findChild(QMenu,  "menu_Profiles")
        self.profile_manager = ProfileManager(profile_menu,  self)
        if len(self.profile_manager.profiles) > 0:
            self.profile = self.profile_manager.profiles[0]
            self.wd = self.profile.path
        else:
            self.profile = None
            self.wd = os.getcwd()
    
    @pyqtSlot()
    def on_action_About_triggered(self):
        """
        Slot documentation goes here.
        """
        about = About()
        about.exec_()
    
    @pyqtSlot()
    def on_actionAbout_Qt_triggered(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        qApp.aboutQt()

    @pyqtSlot()
    def on_action_New_profile_triggered(self):
        profile = ProfileDialog(self.wd,  self)
        cr = profile.exec_()
        if cr:
            self.profile_manager.add_from_dialog(profile)

    @pyqtSlot()
    def setProfile(self):
        action = self.sender()
        profile = self.profile_manager.get_profile(action.text())
        self.wd = profile.path
