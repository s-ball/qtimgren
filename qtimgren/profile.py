#  SPDX-FileCopyrightText: 2025-present s-ball <s-ball@laposte.net>
#  #
#  SPDX-License-Identifier: MIT

"""
Module implementing ProfileDialog.
"""

from PySide6.QtCore import Slot, Qt
from PySide6.QtWidgets import QDialog, QFileDialog, \
    QMessageBox, QWidget, QApplication
import datetime

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
        self.names = [] if names is None else tuple(names)
        if profile is not None:
            self.name.setText(profile.name)
            self.path.setText(profile.path)
            self.pattern.setText(profile.pattern)
            self.use_disk_cache.setChecked(profile.use_disk_cache)

    @Slot()
    def on_change_clicked(self):
        """
        Select the profile folder.
        """
        wd = QFileDialog.getExistingDirectory(
            self, dir=self.path.text(),
            options=QFileDialog.ShowDirsOnly | QFileDialog.DontUseNativeDialog)
        self.path.setText(wd)

    def get_name(self):
        return self.name.text().strip()

    def get_path(self):
        return self.path.text().strip()

    def get_pattern(self):
        return self.pattern.text().strip()

    def get_use_disk_cache(self):
        return self.use_disk_cache.isChecked()

    @Slot()
    def accept(self):
        if self.valid():
            super().accept()

    def valid(self):
        """
        Validate the content of the dialog.
        """
        if self.get_name() in self.names:
            self.error(translate('profile', '"{}" is already used')
                       .format(self.get_name()),
                       Id.translate('profile', 'Name'))
            return False
        if self.get_name() == '':
            self.error(translate('profile', 'Name cannot be empty'),
                       Id.translate('profile', 'Name'))
            return False
        if not os.path.isdir(self.get_path()):
            self.error(translate('profiles', '"{}" is not a valid folder')
                       .format(self.get_path()),
                       Id.translate('profile', 'Path'))
            return False
        now = datetime.datetime.now()
        try:
            now.strftime(self.get_pattern())
        except ValueError:
            self.error(translate('profile',
                                 '"{}" is not a valid date pattern')
                       .format(self.get_pattern()),
                       Id.translate('profile', 'Pattern'))
            return False
        return True

    def error(self, msg, field):
        QMessageBox.warning(self, translate('profile', field), msg)
        attr = 'mask_edit' if field == 'Mask' else field.lower()
        getattr(self, attr).setFocus(Qt.OtherFocusReason)


def translate(ctx, txt):
    return QApplication.instance().translate(ctx, txt)


class Id:
    """
    A quick and dirty hack to force lupdate to collect strings without
    actually translating them (at that point)
    """
    @staticmethod
    def translate(_ctx, txt):
        return txt
