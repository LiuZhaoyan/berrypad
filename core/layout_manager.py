import logging
logger = logging.getLogger(__name__)

import tkinter as tk
from dataclasses import dataclass
from typing import Dict

@dataclass
class LayoutSection:
    """布局区域定义"""
    name: str
    container: tk.Widget
    anchor: str  # 位置标记：'top'、'left'、'right'、'bottom'、'main'
    weight: int = 1  # 空间分配权重
    visible: bool = True

class LayoutManager:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.sections: Dict[str, LayoutSection] = {}
        self.layout_engine = "grid"  # 支持 grid 或 pack
        self._container_cache = {}
        self._setup_main_sections()
        
    def _setup_main_sections(self):
        """创建基础布局区域"""
        # 主内容区域 - 弹性伸缩最大
        self.add_section("main_area", tk.Frame(self.root), "main_left", weight=8)

        # 主内容渲染区域 - 弹性伸缩和主区域一样(待定)
        self.add_section("render_section", tk.Frame(self.root), "main_right", weight=8)
        
        # 顶部工具栏区域
        self.add_section("toolbar_top", tk.Frame(self.root), "top", weight=1)
        
        # 底部状态栏区域
        self.add_section("statusbar_bottom", tk.Frame(self.root), "bottom", weight=1)
        
        # 左侧侧边栏区域
        self.add_section("sidebar_left", tk.Frame(self.root), "left", weight=1)
        
        # 右侧侧边栏区域
        self.add_section("sidebar_right", tk.Frame(self.root), "right", weight=1)
    
    def add_section(self, name: str, container: tk.Widget, anchor: str, weight: int = 1):
        """添加新的布局区域"""
        section = LayoutSection(name, container, anchor, weight)
        self.sections[name] = section
        self._arrange_all_sections()
        return section
    
    def _arrange_all_sections(self):
        """重新排列所有布局区域"""
        # 清除当前布局
        for child in self.root.winfo_children():
            child.grid_forget()
            child.pack_forget()
        
        # 网格布局引擎
        self._arrange_with_grid()
    
    def _arrange_with_grid(self):
        """使用网格布局引擎排列各区域"""
        # 核心布局网格定义
        # TODO: 需要根据section属性调整行列配置
        self.root.grid_rowconfigure(0, weight=1)   # 顶部区域行
        self.root.grid_rowconfigure(1, weight=100)  # 主区域行
        self.root.grid_rowconfigure(2, weight=1)    # 底部区域行
        self.root.grid_columnconfigure(0, weight=1)  # 左侧边栏列
        self.root.grid_columnconfigure(1, weight=100)  # 主区域列
        self.root.grid_columnconfigure(2, weight=100)  # 渲染区域列
        self.root.grid_columnconfigure(3, weight=1)  # 右侧边栏列
        
        # 排列各个区域
        for section in self.sections.values():
            if not section.visible: continue
            
            if section.anchor == "top":
                section.container.grid(row=0, column=0, columnspan=3, sticky="nsew")
            elif section.anchor == "bottom":
                section.container.grid(row=2, column=0, columnspan=3, sticky="nsew")
            elif section.anchor == "left":
                section.container.grid(row=1, column=0, sticky="nsew")
            elif section.anchor == "right":
                section.container.grid(row=1, column=3, sticky="nsew")
            elif section.anchor == "main_left":
                section.container.grid(row=1, column=1, sticky="nsew")
            elif section.anchor == "main_right":
                section.container.grid(row=1, column=2, sticky="nsew")

    def show_section(self, name: str):
        """显示指定区域"""
        if name in self.sections:
            self.sections[name].visible = True
            self._arrange_all_sections()
    
    def hide_section(self, name: str):
        """隐藏指定区域"""
        if name in self.sections:
            self.sections[name].visible = False
            self._arrange_all_sections()
    
    def get_container(self, section_name: str) -> tk.Widget:
        """获取指定布局区域的容器"""
        # 从缓存中直接获取
        if container := self._container_cache.get(section_name):
            return container
        
        # 如果缓存中不存在则查询并添加
        if section := self.sections.get(section_name):
            self._container_cache[section_name] = section.container
            return section.container
        return None

    def invalidate_cache(self):
        """清空容器缓存"""
        self._container_cache.clear()