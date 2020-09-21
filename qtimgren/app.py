#  Copyright (c) 2020  SBA - MIT License

from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QLocale, QTranslator, QLibraryInfo
from .main_window import MainWindow
try:
    from . import resource
except ImportError:
    pass
import sys


def run():
    app = QApplication(sys.argv)
    loc = QLocale()
    qt_trans = QTranslator()
    qt_trans.load(loc, 'qt', '_',
                  QLibraryInfo.location(QLibraryInfo.TranslationsPath))
    app.installTranslator(qt_trans)
    translator = QTranslator()
    translator.load(loc, 'qtimgren', '_', ':')
    app.installTranslator(translator)
    app.setOrganizationName('SBA')
    app.setApplicationName('QtImgren')
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
