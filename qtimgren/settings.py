#  Copyright (c) 2020  SBA - MIT License
from PySide2.QtWidgets import QDialog
from PySide2.QtCore import Qt
from .ui_settings import Ui_settings


class Settings(QDialog, Ui_settings):
    def __init__(self, parent=None, f=Qt.WindowFlags()):
        super().__init__(parent, f)
        self.setupUi(self)
