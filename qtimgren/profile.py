# -*- coding: utf-8 -*-

"""
Module implementing ProfileDialog.
"""

from PyQt5.QtCore import pyqtSlot,  Qt
from PyQt5.QtWidgets import QDialog,  QLineEdit,  QFileDialog,  QCheckBox

from .Ui_profile import Ui_Dialog


class ProfileDialog(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None,  profile=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(ProfileDialog, self).__init__(parent)
        self.setupUi(self)
        self.path = self.findChild(QLineEdit,  "path")
        if profile is not None:
            child = self.findChild(QLineEdit,  'name')
            child.setText(profile.name)
            child = self.findChild(QLineEdit,  'mask')
            child.setText(profile.mask)
            self.path.setText(profile.path)
            child = self.findChild(QCheckBox,  'recurse')
            child.setChecked(profile.recurse)
    
    @pyqtSlot()
    def on_change_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        wd = QFileDialog.getExistingDirectory(self,  directory=self.path.text(),
            options=QFileDialog.ShowDirsOnly | QFileDialog.DontUseNativeDialog)
        self.path.setText(wd)
    
    def getName(self):
        name = self.findChild(QLineEdit,  "name")
        return name.text()
        
    def getPath(self):
        return self.path.text()
        
    def getMask(self):
        mask = self.findChild(QLineEdit,  "mask")
        return mask.text()
        
    def isRecurse(self):
        recurse = self.findChild(QCheckBox,  "recurse")
        return recurse.checkState() == Qt.Checked
