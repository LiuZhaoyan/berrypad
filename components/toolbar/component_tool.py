import tkinter as tk
from tkinter import Menu

from core.component_basic import ComponentBasic
from core.component_manager import ComponentManager


class ComponentTool(ComponentBasic):
    """顶部工具栏组件"""
    def __init__(self, manager, menu_manager):
        super().__init__(name="component_tool", manager=manager)
        self.menu_manager = menu_manager
        
        # 使用布局管理器获取容器
        self.toolbar_frame = self.get_container()
        
        self._init_toolbar()
        # 注意：默认菜单注册移到主应用中
    
    def _init_toolbar(self) -> None:
        """初始化工具栏"""
        # 工具栏框架已经在布局管理器中创建
        # self.toolbar_frame.configure(relief=tk.RAISED, bd=1)
        
        self.manager.subscribe("button_entered", self.on_button_entered)
        self.manager.subscribe("button_leaved", self.on_button_leaved)
    
    def register_default_menus(self) -> None:
        """注册默认菜单 - 由主应用调用"""
        pass  # 实际注册在主应用中完成
    
    def on_button_entered(self, button: tk.Button) -> None:
        """处理按钮悬停事件"""
        button.config(relief=tk.RAISED, bg="#d3d3d3")
    
    def on_button_leaved(self, button: tk.Button) -> None:
        """处理按钮离开事件"""
        button.config(relief=tk.FLAT, bg="SystemButtonFace")
    
    def get_layout_section(self) -> str:
        return "toolbar_top"