# -*- coding: utf-8 -*-

"""
Module implementing ProfilesDialog.
"""

from PyQt5.QtCore import pyqtSlot,  QAbstractTableModel, QModelIndex, Qt
from PyQt5.QtWidgets import QDialog,  QTableView

from .Ui_profiles import Ui_profiles
from .profile import ProfileDialog
from .profile_manager import Profile

class ProfilesModel(QAbstractTableModel):
    def __init__(self,  profiles,  parent=None):
        super().__init__(parent)
        self.profiles = profiles[:]
        
    def rowCount(self,  _parent):
        return len(self.profiles)
    
    def columnCount(self,  _parent):
        return 4
        
    def data(self, index,  role):
        if role != Qt.DisplayRole:
            return None
        p = self.profiles[index.row()]
        col = index.column()
        if col == 0:
            return p.name
        elif col == 1:
            return p.path
        elif col == 2:
            return p.mask
        else:
            return p.recurse
    
    def headerData(self,  section,  orientation,  role):
        headers = ['Name',  'Path',  'Mask',  'recurse']
        if role != Qt.DisplayRole or orientation != Qt.Horizontal:
            return None
        return headers[section]
    
    def set_profile(self,  row,  profile):
        self.profiles[row] = profile
        self.dataChanged.emit(self.createIndex(row,  0),  self.createIndex(row,  3))
    
    def removeRows(self,  row,  count,  parent=QModelIndex()):
        self.beginRemoveRows(parent, row,  row + count - 1)
        del self.profiles[row:row+count]
        self.endRemoveRows()


class ProfilesDialog(QDialog, Ui_profiles):
    """
    Class documentation goes here.
    """
    def __init__(self, profiles,  parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(ProfilesDialog, self).__init__(parent)
        self.setupUi(self)
        self.model = ProfilesModel(profiles)
        self.view = self.findChild(QTableView,  'tableView')
        self.view.setModel(self.model)
    
    @pyqtSlot()
    def on_edit_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        try:
            sel = self.view.selectedIndexes()[0].row()
        except LookupError:
            sel = None
        if sel is not None:
            dialog = ProfileDialog(self,  self.model.profiles[sel])
            cr = dialog.exec_()
            if cr:
                self.model.set_profile(sel,  Profile.from_dialog(dialog))
    
    @pyqtSlot()
    def on_remove_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        sel = self.view.selectedIndexes()
        rows = sorted(set(index.row() for index in sel), reverse=True)
        for row in rows:
            self.model.removeRows(row,  1)
