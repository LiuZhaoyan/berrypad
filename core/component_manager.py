import logging
logger = logging.getLogger(__name__)

from typing import Dict
import tkinter as tk
from core.event_bus import EventBus

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
        if hasattr(component, 'init_hook') and component.init_hook:
            component.init_hook()
        return True
    
    def get_component(self, name: str) -> tk.Widget:
        """获取组件类"""
        return self._components.get(name, None)
    
    def remove_component(self, name: str) -> bool:
        """移除组件"""
        if name in self._components:
            del self._components[name]
            return True
        return False

