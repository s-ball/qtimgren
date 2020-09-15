from PySide2.QtWidgets import QTableView, QStyledItemDelegate, QStyleOptionViewItem
from PySide2.QtCore import QAbstractTableModel, QModelIndex, Qt, Slot, \
    QItemSelection, QItemSelectionModel, QAbstractItemModel, QSize, QRect
from PySide2.QtGui import QImage, QPainter, QPixmap, QPixmapCache
from pyimgren.pyimgren import Renamer, exif_dat
from.profile_manager import Profile
import os.path
import re
import typing
import datetime
from fnmatch import fnmatch


class Model(QAbstractTableModel):
    rx = re.compile(r'.*\.jpe?g*', re.I)

    def __init__(self, profile: Profile, view: QTableView):
        super().__init__(view.parent())
        self.profile = profile
        self.view = view
        self.files = []
        self.orig = {}
        self.renamer = None
        self.ini_files()

    def ini_files(self):
        if self.profile is None:
            self.files = []
            self.orig = {}
            self.renamer = None
        else:
            self.files = [entry.name for entry in os.scandir(self.profile.path)
                          if entry.is_dir() or self.rx.match(entry.name)]
            self.renamer = Renamer(self.profile.path, self.profile.mask,
                                   self.profile.pattern)
            self.orig = self.renamer.load_names()

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self.files)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return 4

    def headerData(self, section:int, orientation:Qt.Orientation,
                   role: int = Qt.DisplayRole) -> typing.Any:
        header = ['Image', 'Name', 'Original', 'New name']
        if orientation == Qt.Orientation.Horizontal and role == Qt.DisplayRole:
            return header[section]

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> typing.Any:
        file = self.files[index.row()]
        if role == Qt.DisplayRole:
            if index.column() == 1:
                return file
            if index.column() == 2:
                return self.orig.get(file, None)
            if index.column() == 3:
                try:
                    dat = exif_dat(os.path.join(self.profile.path, file))
                    if dat is not None:
                        dat += datetime.timedelta(minutes=self.renamer.delta)
                        return dat.strftime(self.profile.pattern)
                except OSError:
                    pass
        elif index.column() == 0:
            if role == Qt.DecorationRole:
                return QImage(os.path.join(self.profile.path, file))
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

    def item_selection(self) -> QItemSelection:
        sel = QItemSelection()
        sel1 = QItemSelection()
        for i, file in enumerate(self.files):
            if fnmatch(file, self.renamer.src_mask):
                sel1.select(self.index(i, 0), self.index(i, 3))
                sel.merge(sel1, QItemSelectionModel.SelectCurrent)
        return sel


class View(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setItemDelegateForColumn(0, ImageDelegate(self))

    def setModel(self, model : QAbstractItemModel):
        super().setModel(model)
        self.reset_selection()

    @Slot()
    def profileChanged(self, profile):
        self.model().profileChanged(profile)
        self.reset_selection()

    @Slot()
    def deltaChanged(self, delta):
        self.model().deltaChanged(delta)

    @Slot()
    def rename(self):
        print(self.selected_files())

    @Slot()
    def back(self):
        selection = self.selectionModel()

    @Slot()
    def reset_selection(self):
        selection = self.selectionModel()
        item_sel = self.model().item_selection()
        selection.select(item_sel, QItemSelectionModel.ClearAndSelect)

    def selected_files(self):
        return [self.model().data(ix, Qt.DisplayRole)
                for ix in self.selectionModel().selectedRows(1)]


class ImageDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cache_key = {}
        QPixmapCache.setCacheLimit(1024000)

    def sizeHint(self, option:QStyleOptionViewItem, index:QModelIndex) -> QSize:
        pixmap = self.get_pixmap(option, index)
        return QSize() if pixmap.isNull() else pixmap.size()

    def paint(self, painter:QPainter, option:QStyleOptionViewItem, index:QModelIndex):
        pixmap = self.get_pixmap(option, index)
        if not pixmap.isNull():
            view = option.styleObject
            view.setRowHeight(index.row(), pixmap.height())
            painter.drawPixmap(option.rect, pixmap)

    def get_pixmap(self, option: QStyleOptionViewItem, index: QModelIndex) -> QPixmap:
        view = option.styleObject
        model = view.model()
        w = view.columnWidth(0)
        file = model.files[index.row()]
        try:
            key = self.cache_key[file]
            pixmap = QPixmapCache.find(key)
            if (pixmap is not None) and (not pixmap.isNull()) and (pixmap.width() != w):
                pixmap = None
        except KeyError:
            pixmap = None
        if pixmap is None:
            image = QImage(os.path.join(model.profile.path, file))
            pixmap = QPixmap.fromImage(image.scaledToWidth(w))
            self.cache_key[file] = QPixmapCache.insert(pixmap)
        return pixmap


