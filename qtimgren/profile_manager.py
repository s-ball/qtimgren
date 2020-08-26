from PyQt5.QtWidgets import QMessageBox


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
        self.profiles = []
        self.parent = parent
        
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
