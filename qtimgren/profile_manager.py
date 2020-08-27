from PyQt5.QtWidgets import QMessageBox,  qApp,  QActionGroup
from PyQt5.QtCore import QSettings


class Profile:
    def __init__(self,  name,  path,  mask,  recurse):
        self.name = name
        self.path = path
        self.mask = mask
        self.recurse = recurse
        
    @staticmethod
    def from_dialog(self,  dialog):
        return Profile(dialog.getName(),  dialog.getPath(), 
            dialog.getMask(),  dialog.isRecurse())


class ProfileManager:
    def __init__(self, menu, parent=None):
        self.menu = menu
        actions = self.menu.actions()
        self.tail = actions[-2:]
        self.head = actions[:2]
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
            self.actGroup.triggered.connect(self.parent.setProfileGroup)
            self.actGroup.triggered.connect(self.set_active_profile)
            self.menu.removeAction(self.tail[0])
            self.menu.removeAction(self.tail[1])
            active = settings.value('active_profile')
            self.active_profile = self.get_profile(active)
            for name in self.names():
                action = self.menu.addAction(name)
                action.setCheckable(True)
                self.actGroup.addAction(action)
                if name == active:
                    action.setChecked(True)
            self.menu.addActions(self.tail)

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
            self.menu.removeAction(self.tail[0])
            self.menu.removeAction(self.tail[1])
            action = self.menu.addAction(name)
            action.setCheckable(True)
            self.actGroup.addAction(action)
            self.menu.addActions(self.tail)
            
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
