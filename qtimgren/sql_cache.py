#  SPDX-FileCopyrightText: 2025-present s-ball <s-ball@laposte.net>
#  #
#  SPDX-License-Identifier: MIT
import abc
import os.path
import sqlite3
import threading
from collections.abc import Callable, Collection

from PySide6.QtCore import QBuffer, QIODevice
from PySide6.QtGui import QImage


class AbstractCache(abc.ABC):
    def close(self):
        pass

    @abc.abstractmethod
    def get_thumbnail(self, file: str) -> QImage:
        pass

    def get_status(self, files: Collection[str]) -> tuple[int, int, int]:
        return 0, len(files), 0

    def clean(self, files: Collection[str]) -> int:
        return 0

    def prune(self) -> int:
        return 0

    def load(self, files: Collection[str]):
        pass


class SQLiteCache(AbstractCache):
    base = 'qtimgren.sqlite'
    sz = 256
    fmt = 'PNG'

    def __init__(self, folder: str, get_name: Callable[[str], str]):
        self.main_lock = threading.Lock()
        self.locks: dict[str, threading.Lock] = {}
        self.load_thread: threading.Thread = None
        self.load_files: list[str] = []
        self.stop_thread = False
        self.folder = folder
        self.get_name = get_name
        self.con = sqlite3.connect(os.path.join(folder, self.base), check_same_thread=False)
        self._closed = False
        curs = self.con.cursor()
        curs.execute("""CREATE TABLE IF NOT EXISTS thumbnails("""
                     """name TEXT PRIMARY KEY,"""
                     """thumbnail BLOB)"""
        )

    def close(self, commit=True):
        if not self._closed:
            if self.load_thread:
                self.stop_thread = True
                self.load_thread.join()
            if commit:
                self.con.commit()
            self.con.close()
            self._closed = True

    def __del__(self):
        self.close()

    def get_thumbnail(self, file: str) -> QImage:
        curs = self.con.cursor()
        name = self.get_name(file)
        self._require(name)
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
        self._release(name)
        return im

    def _require(self, name):
        self.main_lock.acquire()
        wait: threading.Lock = None
        while name in self.locks:
            if wait:
                wait.release()
            wait = self.locks[name]
            self.main_lock.release()
            wait.acquire()
            self.main_lock.acquire()
        if wait:
            wait.release()
        self.locks[name] = threading.Lock()
        self.locks[name].acquire()
        self.main_lock.release()

    def _release(self, name):
        self.main_lock.acquire()
        self.locks[name].release()
        del self.locks[name]
        self.main_lock.release()

    def get_pixmap(self, file: str, w: int) -> QImage:
        im = self.get_thumbnail(file)
        im = im.scaledToWidth(w)
        return im

    def _cached(self) -> set[str]:
        curs = self.con.cursor()
        curs.execute("SELECT name FROM thumbnails")
        cached = set(row[0] for row in curs.fetchall())
        return cached

    def get_status(self, files: Collection[str]) -> tuple[int, int, int]:
        cached = self._cached()
        files = set(self.get_name(f) for f in files)
        nb_cached = len(cached.intersection(files))
        nb_files = len(files)
        nb_tot = len(cached)
        return nb_cached, nb_files, nb_tot

    def clean(self, files: Collection[str]) -> int:
        cached = self._cached()
        files = set(self.get_name(f) for f in files)
        curs = self.con.cursor().executemany(
            "DELETE FROM thumbnails WHERE name=?",
            [(i,) for i in cached.difference(files)]
        )
        return curs.rowcount

    def prune(self) -> int:
        curs = self.con.cursor().execute("DELETE FROM thumbnails")
        return curs.rowcount

    def load(self, files: Collection[str]):
        if self.load_thread is not None:
            self.stop_thread = True
            self.load_thread.join()
        self.load_thread = threading.Thread(target=self._do_load,
                                            args=(files,))
        self.stop_thread = False
        self.load_thread.start()

    def _do_load(self, files: Collection[str]):
        for file in files:
            if self.stop_thread:
                break
            self.get_thumbnail(file)


class NullCache(AbstractCache):
    def __init__(self, folder: str, _get_name: Callable[[str], str]):
        self.folder = folder

    def get_thumbnail(self, file: str) -> QImage:
        return QImage(os.path.join(self.folder, file))


def get_cache(use_disk_cache, folder: str, get_name: Callable[[str], str]
              ) -> AbstractCache:
    cache_type = SQLiteCache if use_disk_cache else NullCache
    return cache_type(folder, get_name)