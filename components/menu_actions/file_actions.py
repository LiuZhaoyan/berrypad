
from core.component_basic import MenuActionComponent


class NewFileAction(MenuActionComponent):
    def execute(self):
        self.manager.publish("file.new")

class OpenFileAction(MenuActionComponent):
    def execute(self):
        self.manager.publish("file.open")

class SaveFileAction(MenuActionComponent):
    def execute(self):
        self.manager.publish("file.save")

class SaveAsFileAction(MenuActionComponent):
    def execute(self):
        self.manager.publish("file.save_as")