from PyQt5.QtWidgets import QMessageBox,  qApp,  QActionGroup,  QAction
from PyQt5.QtCore import QSettings,  QObject,  pyqtSignal


class Profile:
    def __init__(self,  name,  path,  mask,  recurse):
        self.name = name
        self.path = path
        self.mask = mask
        self.recurse = recurse
        
    @staticmethod
    def from_dialog(dialog):
        return Profile(dialog.getName(),  dialog.getPath(), 
            dialog.getMask(),  dialog.isRecurse())


class ProfileManager(QObject):
    profileChanged = pyqtSignal()
    def __init__(self, menu, parent=None):
        super().__init__(parent)
        self.menu = menu
        actions = self.menu.actions()
        self.sep= actions[-2]
        self.parent = parent
        self.profiles = []
        self.actGroup = None
        self.active_profile = None
        self.load()
        qApp. aboutToQuit.connect(self.save)
        
    def load(self):
        settings = QSettings()
        settings.beginGroup('profiles')
        groups = settings.childGroups()
        self.profiles = [Profile(p,  settings.value(f'{p}/path'), 
                                   settings.value(f'{p}/mask'), 
                                   settings.value(f'{p}/recurse'))
                        for p in groups]
        settings.endGroup()
        if len(self.profiles) > 0:
            self.actGroup = QActionGroup(self.parent)
            self.actGroup.triggered.connect(self.set_active_profile)
            active = settings.value('active_profile')
            self.active_profile = self.get_profile(active)
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
            settings.setValue(f'{p.name}/mask',  p.mask)
            settings.setValue(f'{p.name}/recurse',  p.recurse)
        settings.endGroup()
        if self.active_profile is not None:
            settings.setValue('active_profile',  self.active_profile.name)
        
    def names(self):
        for p in self.profiles:
            yield p.name
    
    def add_action(self, name, path, mask, recurse):
        if name in self.names():
            QMessageBox.warning(self.parent,  None,  '{} already exists'.format(name))
        else:
            self.profiles.append(Profile(name,  path,  mask,  recurse))
            self.do_add_action(name)
    
    def do_add_action(self,  name):
            action = QAction(name,  self.menu)
            self.menu.insertAction(self.sep,  action)
            action.setCheckable(True)
            self.actGroup.addAction(action)
            return action
            
    def add_from_dialog(self,  dialog):
        self.add_action(dialog.getName(),  dialog.getPath(),
                dialog.getMask(),  dialog.isRecurse())

    def get_profile(self,  name):
        for p in self.profiles:
            if name == p.name:
                return p
        return None

    def set_active_profile(self):
        action = self.actGroup.checkedAction()
        self.active_profile = self.get_profile(action.text())
        self.profileChanged.emit()
    
    def reset_profiles(self,  profiles):
        self.clear_menu()
        self.profiles = profiles
        if len(profiles) > 0:
            if self.active_profile.name not in (p.name for p in profiles):
                active = profiles[0].name
                self.active_profile = self.get_profile(active)
            else:
                active = self.active_profile.name
            for name in self.names():
                action = self.do_add_action(name)
                if name == active:
                    action.setChecked(True)
            self.profileChanged.emit()
    
    def clear_menu(self):
        while len(self.actGroup.actions()) > 0:
            self.actGroup.removeAction(self.actGroup.actions()[0])

