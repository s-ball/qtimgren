#  SPDX-FileCopyrightText: 2025-present s-ball <s-ball@laposte.net>
#  #
#  SPDX-License-Identifier: MIT

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QLocale, QTranslator, QLibraryInfo, QDir, QSettings
from PySide6.QtGui import QIcon
from .main_window import MainWindow
import argparse

try:
    from . import rc_qtimgren
except ImportError:
    pass
import sys


class Application(QApplication):
    known_lang = {'C': QApplication.translate('app', 'English'),
                  'fr': QApplication.translate('app', 'French')}

    def __init__(self, argv):
        params = parse(sys.argv[1:])[0]
        super().__init__(argv)
        self.setOrganizationName('s-ball')
        self.setApplicationName('QtImgren')
        if params.lang is None:
            settings = QSettings()
            lang = settings.value('MainWindow/lang')
            loc = QLocale() if lang is None else QLocale(lang)
        elif params.lang == 'native':
            loc = QLocale()
        else:
            loc = QLocale(params.lang)
        self.translator = QTranslator()
        self.qt_trans = QTranslator()
        if self.translator.load(loc, '', '', ':/lang', ''):
            self.qt_trans.load(loc, 'qtbase', '_', QLibraryInfo
                               .location(QLibraryInfo.TranslationsPath))
        self.installTranslator(self.qt_trans)
        self.installTranslator(self.translator)
        self.setWindowIcon(QIcon(':/icon/app.ico'))
        self.main_window = MainWindow()

    def set_language(self, lang):
        self.removeTranslator(self.translator)
        self.removeTranslator(self.qt_trans)
        loc = QLocale(lang)
        self.qt_trans.load(loc, 'qt', '_',
                           QLibraryInfo.location(QLibraryInfo.TranslationsPath))
        self.installTranslator(self.qt_trans)
        self.translator.load(loc, '', '', ':/lang', '')
        self.installTranslator(self.translator)

    def get_language(self):
        lang = self.translator.language()
        return 'C' if (lang is None or lang == '') else lang

    def get_languages(self):
        yield 'C', self.translate('app', 'English')
        for lang in QDir(':/lang').entryList():
            l = lang
            loc = QLocale(lang)
            if lang in self.known_lang:
                name = self.translate('app', self.known_lang[lang])
            else:
                name = loc.nativeLanguageName()
            t = QTranslator()
            if t.load(loc, '', '', ':/lang', ''):
                l = t.language()
            yield l, name


def parse(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--lang', '-l',
                        help='force a specific language (or native)')
    return parser.parse_known_args(argv)


def run():
    app = Application(sys.argv)
    app.main_window.show()
    sys.exit(app.exec_())
