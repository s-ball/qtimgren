# -*- coding: utf-8 -*-

"""
Module implementing ProfileDialog.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog,  QLineEdit,  QFileDialog,  QCheckBox

from .Ui_profile import Ui_Dialog


class ProfileDialog(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, wd,  parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(ProfileDialog, self).__init__(parent)
        self.wd = wd
        self.setupUi(self)
        self.path = self.findChild(QLineEdit,  "path")
        self.path.setText(wd)
        
    
    @pyqtSlot()
    def on_change_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.wd = QFileDialog.getExistingDirectory(self,  directory=self.wd,
            options=QFileDialog.ShowDirsOnly | QFileDialog.DontUseNativeDialog)
        self.path.setText(self.wd)
    
    def getName(self):
        name = self.findChild(QLineEdit,  "name")
        return name.text()
        
    def getPath(self):
        return self.wd
        
    def getMask(self):
        mask = self.findChild(QLineEdit,  "mask")
        return mask.text()
        
    def isRecurse(self):
        recurse = self.findChild(QCheckBox,  "recurse")
        return recurse.checkState()