from dataclasses import dataclass
from typing import Callable, List
from core.component_manager import ComponentManager
import tkinter as tk

@dataclass
class ComponentBasic:
    """编辑器组件基类"""
    manager: ComponentManager
    name: str
    widget: tk.Widget = None
    dependencies: List[str] = None
    init_hook: Callable = None


    def __post_init__(self):
        """组件初始化后处理"""
        if self.manager:
            # 自动注册组件到管理器
            self.manager.register_component(self)
            
    def create_gui(self, container: tk.Widget) -> None:
        """组件GUI创建方法(子类实现)"""
        # logger.info(f"创建组件UI: {self.name}")
        pass
    
    def post_layout_init(self) -> None:
        """布局完成后执行的初始化（可重写）"""
        # logger.info(f"布局完成后初始化组件: {self.name}")
        pass
    
    def get_container(self) -> tk.Widget:
        """获取组件的布局容器"""
        if self.manager and self.manager.layout_manager:
            # 直接访问带有缓存的获取方法
            return self.manager.layout_manager.get_container(self.get_layout_section())
        return None
    
    def destroy_widget(self) -> None:
        """销毁组件的GUI小部件"""
        if self.widget:
            self.widget.destroy()
            self.widget = None
            # logger.info(f"销毁组件小部件: {self.name}")

    def get_layout_section(self) -> str:
        """返回组件的主要布局区域（默认主区域）"""
        return "main_area"
    
    @staticmethod
    def check_direct_text_child(frame) -> tk.Widget:
        """检查是否有直接的文本子组件"""
        for child in frame.winfo_children():
            if isinstance(child, tk.Text):
                return child
        return None

class MenuActionComponent:
    """菜单动作组件基类"""
    def __init__(self, name: str, manager):
        self.name = name
        self.manager = manager
        # self.manager.register_component(self) # TODO: 是否需要注册？
    
    def execute(self, *args, **kwargs):
        """执行菜单动作"""
        raise NotImplementedError("子类必须实现 execute 方法")