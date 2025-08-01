from core.component_basic import MenuActionComponent


class CopyAction(MenuActionComponent):
    def execute(self):
        self.manager.publish("edit.copy")

class PasteAction(MenuActionComponent):
    def execute(self):
        self.manager.publish("edit.paste")

class CutAction(MenuActionComponent):
    def execute(self):
        self.manager.publish("edit.cut")
