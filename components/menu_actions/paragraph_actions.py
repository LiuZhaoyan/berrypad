from core.component_basic import MenuActionComponent


class HeadingAction(MenuActionComponent):
    def execute(self, num):
        self.manager.publish(f"paragraph.heading{num}")
    def execute_1(self):
        self.manager.publish("paragraph.heading1")
    def execute_2(self):
        self.manager.publish("paragraph.heading2")
    def execute_3(self):
        self.manager.publish("paragraph.heading3")
    def execute_4(self):
        self.manager.publish("paragraph.heading4")
    def execute_5(self):
        self.manager.publish("paragraph.heading5")
    def execute_6(self):
        self.manager.publish("paragraph.heading6")

class QuoteAction(MenuActionComponent):
    def execute(self):
        self.manager.publish("paragraph.quote")

class UnorderedListAction(MenuActionComponent):
    def execute(self):
        self.manager.publish("paragraph.unordered_list")

class OrderedListAction(MenuActionComponent):
    def execute(self):
        self.manager.publish("paragraph.ordered_list")

class CodeBlockAction(MenuActionComponent):
    def execute(self):
        self.manager.publish("paragraph.code_block")
