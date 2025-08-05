
from core.component_basic import MenuActionComponent


class FontSelectAction(MenuActionComponent):
    """字体选择动作"""
    def __init__(self, name: str, manager, font_family: str):
        super().__init__(name, manager)
        self.font_family = font_family
    
    def execute(self):
        """执行字体选择"""
        # 发布字体选择事件
        self.manager.publish("theme.font_selected", font_family=self.font_family)
        
class FontSizeIncreaseAction(MenuActionComponent):
    """增大字体动作"""
    def execute(self):
        self.manager.publish("theme.font_size_increase")

class FontSizeDecreaseAction(MenuActionComponent):
    """减小字体动作"""
    def execute(self):
        self.manager.publish("theme.font_size_decrease")

class FontSizeResetAction(MenuActionComponent):
    """重置字体动作"""
    def execute(self):
        self.manager.publish("theme.font_size_reset")