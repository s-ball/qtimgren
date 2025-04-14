#  SPDX-FileCopyrightText: 2025-present s-ball <s-ball@laposte.net>
#  #
#  SPDX-License-Identifier: MIT
import os.path
import sqlite3
from collections.abc import Callable

from PySide6.QtCore import QBuffer, QIODevice
from PySide6.QtGui import QImage


class SQLiteCache:
    base = 'qtimgren.sqlite'
    sz = 256
    fmt = 'PNG'

    def __init__(self, folder: str, get_name: Callable[[str], str]):
        self.folder = folder
        self.get_name = get_name
        self.con = sqlite3.connect(os.path.join(folder, self.base))
        self._closed = False
        curs = self.con.cursor()
        curs.execute("""CREATE TABLE IF NOT EXISTS thumbnails("""
                     """name TEXT PRIMARY KEY,"""
                     """thumbnail BLOB)"""
        )

    def close(self, commit=True):
        if not self._closed:
            if commit:
                self.con.commit()
            self.con.close()
            self._closed = True

    def __del__(self):
        self.close()

    def get_thumbnail(self, file: str) -> QImage:
        curs = self.con.cursor()
        name = self.get_name(file)
        curs.execute("""SELECT thumbnail FROM thumbnails WHERE name=?""",
                     (name,))
        row = curs.fetchone()
        if row:
            im = QImage()
            im.loadFromData(row[0], self.fmt)
        else:
            im = QImage(os.path.join(self.folder, file))
            im = im.scaledToWidth(self.sz)
            buf = QBuffer()
            buf.open(QIODevice.OpenModeFlag.WriteOnly)
            im.save(buf, self.fmt)
            curs.execute("INSERT INTO thumbnails VALUES(?,?)",
                         (name, buf.buffer().data()))
            buf.close()
        return im

    def get_pixmap(self, file: str, w: int) -> QImage:
        im = self.get_thumbnail(file)
        im = im.scaledToWidth(w)
        return im