from PyQt5.QtWidgets import QMessageBox,  qApp
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
            self.menu.removeAction(self.tail[0])
            self.menu.removeAction(self.tail[1])
            for name in self.names():
                action = self.menu.addAction(name)
                action.triggered.connect(self.parent.setProfile)
            self.menu.addActions(self.tail)

    def save(self):
        settings = QSettings()
        settings.beginGroup('profiles')
        settings.remove('')
        for p in self.profiles:
            settings.setValue(f'{p.name}/path',  p.path)
            settings.setValue(f'{p.name}/mask',  p.mask)
            settings.setValue(f'{p.name}/recurse',  p.recurse)
        
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
            action.triggered.connect(self.parent.setProfile)
            self.menu.addActions(self.tail)
            
    def add_from_dialog(self,  dialog):
        self.add_action(dialog.getName(),  dialog.getPath(),
                dialog.getMask(),  dialog.isRecurse())

    def get_profile(self,  name):
        for p in self.profiles():
            if name == p.name:
                return p
        return None
