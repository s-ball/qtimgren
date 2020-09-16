from PySide2.QtWidgets import QTableView, QStyledItemDelegate, \
    QStyleOptionViewItem, QApplication
from PySide2.QtCore import QAbstractTableModel, QModelIndex, Qt, Slot, \
    QItemSelection, QItemSelectionModel, QAbstractItemModel, QSize, \
    QTimer, QSettings
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
        QApplication.instance().aboutToQuit.connect(self.save)

    def initialize(self, model : QAbstractItemModel, images_display):
        super().setModel(model)
        self.images_display = images_display
        self.load()
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

    @Slot()
    def save(self):
        settings = QSettings()
        settings.beginGroup('View')
        settings.beginWriteArray('col_size')
        for i in range(3):
            settings.setArrayIndex(i)
            settings.setValue('col', self.columnWidth(i))
        settings.endArray()
        settings.setValue('display_images',
                          self.images_display.checkState() == Qt.Checked)
        settings.endGroup()

    @Slot()
    def select_renamed(self):
        pass

    @Slot()
    def display_images(self, display):
        self.setColumnHidden(0, not display)

    def load(self):
        settings = QSettings()
        settings.beginGroup('View')
        sz = settings.beginReadArray('col_size')
        for i in range(sz):
            settings.setArrayIndex(i)
            w = settings.value('col')
            self.setColumnWidth(i, w)
        settings.endArray()
        display = settings.value('display_images', type=bool)
        if not display:
            self.setColumnHidden(0, True)
        self.images_display.setCheckState(Qt.Checked if display
                                          else Qt.Unchecked)
        settings.endGroup()
        delegate = ImageDelegate(self)
        self.setItemDelegateForColumn(0, delegate)
        self.pre_load(delegate)


    def selected_files(self):
        return [self.model().data(ix, Qt.DisplayRole)
                for ix in self.selectionModel().selectedRows(1)]

    def pre_load(self, delegate):
        view = self
        model = view.model()
        width = view.columnWidth(0)
        cur = 0
        timer = QTimer(view)

        def step():
            nonlocal width, cur, model
            if view.model() is not model:
                cur = 0
                model = view.model()
            if view.columnWidth(0) != 0 and view.columnWidth(0) != width:
                cur = 0
                width = view.columnWidth(0)
            if cur < len(model.files) and width != 0:
                print(cur, len(model.files), width)
                delegate._do_get_pixmap(model, cur, width)
                cur += 1
            if cur >= len(model.files):
                timer.setInterval(1000)
            else:
                timer.setInterval(0)

        timer.timeout.connect(step)
        timer.start()


class ImageDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cache_key = {}
        QPixmapCache.setCacheLimit(102400)

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
        return self._do_get_pixmap(model, index.row(), w)

    def _do_get_pixmap(self, model, row, w):
        if w == 0:
            return QPixmap()
        file = model.files[row]
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
            print(file, pixmap, w)
        return pixmap
