# -*- coding: utf-8 -*-

"""
Module implementing ProfileDialog.
"""

from PyQt5.QtCore import pyqtSlot,  Qt
from PyQt5.QtWidgets import QDialog,  QLineEdit,  QFileDialog,  QCheckBox,  \
    QMessageBox

import os.path

from .Ui_profile import Ui_Dialog


class ProfileDialog(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None,  profile=None,  names=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(ProfileDialog, self).__init__(parent)
        self.setupUi(self)
        self.path = self.findChild(QLineEdit,  "path")
        self.names = [] if names is None else tuple(names)
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
        wd = QFileDialog.getExistingDirectory(self,  directory=self.path.text(),
            options=QFileDialog.ShowDirsOnly | QFileDialog.DontUseNativeDialog)
        self.path.setText(wd)
    
    def getName(self):
        name = self.findChild(QLineEdit,  "name")
        return name.text().strip()
        
    def getPath(self):
        return self.path.text().strip()
        
    def getMask(self):
        mask = self.findChild(QLineEdit,  "mask")
        return mask.text().strip()
        
    def isRecurse(self):
        recurse = self.findChild(QCheckBox,  "recurse")
        return recurse.checkState() == Qt.Checked

    @pyqtSlot()
    def on_buttonBox_accepted(self):
        if self.valid():
            self.accept()

    def valid(self):
        if self.getName() in self.names:
            self.error('"{}" is already used'.format(self.getName()), 'name')
            return False
        if self.getName() == '':
            self.error('Name cannot be empty',  'name')
            return False
        if not os.path.isdir(self.getPath()):
            self.error('"{}" is not a valid folder'.format(self.getPath()), 
                           'path')
            return False
        if '*' not in self.getMask() and '?' not in self.getMask():
            self.error('"{}" is not a valid image pattern'.format(
                            self.getMask()), 'mask')
            return False
        return True

    def error(self,  msg,  field):
        QMessageBox.warning(self,  field.capitalize(),  msg)
        self.findChild(QLineEdit,  field).setFocus(Qt.OtherFocusReason)
