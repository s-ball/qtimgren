#  SPDX-FileCopyrightText: 2025-present s-ball <s-ball@laposte.net>
#  #
#  SPDX-License-Identifier: MIT

from PySide6.QtGui import QAction, QActionGroup
from PySide6.QtWidgets import QMessageBox,  QApplication
from PySide6.QtCore import QSettings,  QObject,  Signal


defaultPattern = '%Y%m%d_%H%M%S.jpg'


class Profile:
    def __init__(self,  name,  path,  pattern=defaultPattern,
                 use_disk_cache: bool = True):
        self.name = name
        self.path = path
        self.pattern = pattern
        self.use_disk_cache = use_disk_cache
        
    @staticmethod
    def from_dialog(dialog):
        return Profile(dialog.get_name(), dialog.get_path(),
                       dialog.get_pattern(), dialog.get_use_disk_cache())


class ProfileManager(QObject):
    profile_changed = Signal(Profile)

    def __init__(self, menu, parent=None):
        super().__init__(parent)
        self.menu = menu
        actions = self.menu.actions()
        self.sep = actions[-2]
        self.parent = parent
        self.profiles = []
        self.actGroup = None
        self.active_profile = None
        self.load()
        QApplication.instance().aboutToQuit.connect(self.save)
        
    def load(self):
        settings = QSettings()
        settings.beginGroup('profiles')
        groups = settings.childGroups()
        self.profiles = [Profile(p,  settings.value(f'{p}/path'),
                                 settings.value(f'{p}/pattern'),
                                 settings.value(f'{p}/use_disk_cache',
                                                True, type=bool))
                         for p in groups]
        settings.endGroup()
        self.actGroup = QActionGroup(self.parent)
        self.actGroup.triggered.connect(self.set_active_profile)
        active = settings.value('active_profile')
        self.active_profile = self.get_profile(active)
        if len(self.profiles) > 0:
            for name in self.names():
                action = self.do_add_action(name)
                if name == active:
                    action.setChecked(True)

    def save(self):
        settings = QSettings()
        settings.beginGroup('profiles')
        settings.remove('')
        for p in self.profiles:
            settings.setValue(f'{p.name}/path',  p.path)
            settings.setValue(f'{p.name}/pattern',  p.pattern)
            settings.setValue(f'{p.name}/use_disk_cache',  p.use_disk_cache)
        settings.endGroup()
        if self.active_profile is not None:
            settings.setValue('active_profile',  self.active_profile.name)
        
    def names(self):
        for p in self.profiles:
            yield p.name
    
    def add_action(self, name, path, pattern):
        if name in self.names():
            app = QApplication.instance()
            QMessageBox.warning(self.parent,  app.applicationName(),
                                app.translate('profile_manager',
                                              '{} already exists')
                                .format(name))
        else:
            self.profiles.append(Profile(name,  path,  pattern))
            self.do_add_action(name)
    
    def do_add_action(self,  name):
        action = QAction(name,  self.menu)
        self.menu.insertAction(self.sep,  action)
        action.setCheckable(True)
        self.actGroup.addAction(action)
        return action
            
    def add_from_dialog(self,  dialog):
        self.add_action(dialog.get_name(), dialog.get_path(),
                        dialog.get_pattern())

    def get_profile(self,  name):
        for p in self.profiles:
            if name == p.name:
                return p
        return None

    def set_active_profile(self):
        action = self.actGroup.checkedAction()
        self.active_profile = self.get_profile(action.text()) if action \
            is not None else None
        self.profile_changed.emit(self.active_profile)
    
    def reset_profiles(self,  profiles):
        self.clear_menu()
        self.profiles = profiles
        if len(profiles) > 0:
            if self.active_profile.name not in (p.name for p in profiles):
                active = profiles[0].name
            else:
                active = self.active_profile.name
            for name in self.names():
                action = self.do_add_action(name)
                if name == active:
                    action.setChecked(True)
        else:
            active = None
        self.active_profile = self.get_profile(active)
        self.profile_changed.emit(self.active_profile)

    def clear_menu(self):
        while len(self.actGroup.actions()) > 0:
            self.actGroup.removeAction(self.actGroup.actions()[0])
