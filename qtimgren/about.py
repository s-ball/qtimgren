# -*- coding: utf-8 -*-

"""
Module implementing About.
"""

from PySide2.QtWidgets import QDialog,  QLabel

from .ui_about import Ui_About
from . import __version__
from pyimgren import __version__ as libversion


class About(QDialog, Ui_About):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(About, self).__init__(parent)
        self.setupUi(self)
        version = self.findChild(QLabel, 'version')
        version.setText(version.text() + __version__)
        liblabel = self.findChild(QLabel,  'libversion')
        liblabel.setText(liblabel.text().replace('0.0.0',  libversion))
