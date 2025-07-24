from typing import Dict, List, Callable
from dataclasses import dataclass
import tkinter as tk
from bus import EventBus

class ComponentManager(EventBus):
    """组件管理器"""
    def __init__(self, root, layout_manager=None):
        super().__init__()
        self.root = root
        self.layout_manager = layout_manager
        self._components: Dict = {}
        
    def register_component(self, component) -> bool:
        """注册组件"""
        if component.name in self._components:
            # logging.warning(f"组件已存在: {component.name}")
            return False
            
        self._components[component.name] = component
        # logging.info(f"已注册组件: {component.name}")
        
        # 执行初始化钩子
        if component.init_hook:
            component.init_hook()
        return True
    
    def get_component(self, name: str) -> tk.Widget:
        """获取组件"""
        return self._components.get(name, None)

@dataclass
class ComponentBasic:
    """编辑器组件基类"""
    manager: ComponentManager # 组件管理器引用
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
