from core.component_basic import MenuActionComponent

class StrongAction(MenuActionComponent):
    def execute(self):
        self.manager.publish("format.strong")

class EmphasisAction(MenuActionComponent):
    def execute(self):
        self.manager.publish("format.emphasis")

class UnderlineAction(MenuActionComponent):
    def execute(self):
        self.manager.publish("format.underline")

class CodeAction(MenuActionComponent):
    def execute(self):
        self.manager.publish("format.code")

class StrikeAction(MenuActionComponent):
    def execute(self):
        self.manager.publish("format.strike")