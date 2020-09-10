# -*- coding: utf-8 -*-

"""
Module implementing ProfileDialog.
"""

from PySide2.QtCore import Slot, Qt
from PySide2.QtWidgets import QDialog, QLineEdit, QFileDialog, QCheckBox, \
    QMessageBox, QWidget, QApplication

import os.path
from typing import Optional

from .ui_profile import Ui_Dialog


class ProfileDialog(QDialog, Ui_Dialog):
    """
    A dialog for creation or edition of a profile.
    """
    def __init__(self, parent: Optional[QWidget] = None,
                 profile=None, names=None):
        """
        Constructor.

        @param parent reference to the parent widget
        @param profile an optional profile to edit
        @param names
        """
        super(ProfileDialog, self).__init__(parent)
        self.setupUi(self)
        self.path = self.findChild(QLineEdit, "path")
        self.names = [] if names is None else tuple(names)
        if profile is not None:
            child = self.findChild(QLineEdit, 'name')
            child.setText(profile.name)
            child = self.findChild(QLineEdit, 'mask')
            child.setText(profile.mask)
            self.path.setText(profile.path)
            child = self.findChild(QCheckBox, 'recurse')
            child.setChecked(profile.recurse)

    @Slot()
    def on_change_clicked(self):
        """
        Select the profile folder.
        """
        wd = QFileDialog.getExistingDirectory(
            self, directory=self.path.text(),
            options=QFileDialog.ShowDirsOnly | QFileDialog.DontUseNativeDialog)
        self.path.setText(wd)

    def getName(self):
        name = self.findChild(QLineEdit, "name")
        return name.text().strip()

    def getPath(self):
        return self.path.text().strip()

    def getMask(self):
        mask = self.findChild(QLineEdit, "mask")
        return mask.text().strip()

    def isRecurse(self):
        recurse = self.findChild(QCheckBox, "recurse")
        return recurse.checkState() == Qt.Checked

    @Slot()
    def on_buttonBox_accepted(self):
        if self.valid():
            self.accept()

    def valid(self):
        """
        Validate the content of the dialog.
        """
        if self.getName() in self.names:
            self.error(translate('profile', '"{}" is already used')
                       .format(self.getName()), 'name')
            return False
        if self.getName() == '':
            self.error(translate('profile', 'Name cannot be empty'),
                       'name')
            return False
        if not os.path.isdir(self.getPath()):
            self.error(translate('profiles', '"{}" is not a valid folder')
                       .format(self.getPath()), 'path')
            return False
        if '*' not in self.getMask() and '?' not in self.getMask():
            self.error(translate('profile',
                                 '"{}" is not a valid image pattern')
                       .format(self.getMask()), 'mask')
            return False
        return True

    def error(self, msg, field):
        QMessageBox.warning(self, field.capitalize(), msg)
        self.findChild(QLineEdit, field).setFocus(Qt.OtherFocusReason)


def translate(ctx, txt):
    return QApplication.instance().translate(ctx, txt)
