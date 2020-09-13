from PySide2.QtWidgets import QTableView
from PySide2.QtCore import QAbstractTableModel, QModelIndex, Qt, Slot
from pyimgren import Renamer, pyimgren
import os.path
import re
import typing
import datetime

class Model(QAbstractTableModel):
    rx = re.compile(r'.*\.jpe?g*', re.I)

    def __init__(self, profile, view:QTableView):
        super().__init__(view.parent())
        self.profile = profile
        self.view = view
        self.ini_files()
        self.renamer = None if profile is None else Renamer(
            profile.path, profile.mask, profile.pattern)
        self.orig = {} if profile is None else self.renamer.load_names()
        view.setModel(self)

    def ini_files(self):
        if self.profile is None:
            self.files = []
        else:
            self.files = [entry.name for entry in os.scandir(self.profile.path)
                          if entry.is_dir() or self.rx.match(entry.name)]

    def rowCount(self, parent:QModelIndex=QModelIndex()) -> int:
        return len(self.files)

    def columnCount(self, parent:QModelIndex=QModelIndex()) -> int:
        return 4

    def headerData(self, section:int, orientation:Qt.Orientation,
                   role:int=Qt.DisplayRole) -> typing.Any:
        header = ['Image', 'Name', 'Original', 'New name']
        if orientation == Qt.Orientation.Horizontal and role == Qt.DisplayRole:
            return header[section]

    def data(self, index:QModelIndex, role:int=Qt.DisplayRole) -> typing.Any:
        if role == Qt.DisplayRole:
            file = self.files[index.row()]
            if index.column() == 1:
                return file
            if index.column() == 2:
                return self.orig.get(file, None)
            if index.column() == 3:
                dat = pyimgren.exif_dat(os.path.join(self.profile.path, file))
                if dat is not None:
                    dat += datetime.timedelta(minutes=self.renamer.delta)
                    return dat.strftime(self.profile.pattern)
        return None

    @Slot()
    def profileChanged(self, profile):
        self.beginResetModel()
        self.profile = profile
        self.ini_files()
        self.endResetModel()

    @Slot()
    def deltaChanged(self, delta):
        self.renamer.delta = delta
        self.dataChanged.emit(self.index(0, 3),
                               self.index(self.rowCount() - 1, 3))