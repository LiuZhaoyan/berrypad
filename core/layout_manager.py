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
    visible: bool = True

class LayoutManager:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.sections: Dict[str, LayoutSection] = {}
        self.layout_engine = "grid"  # 支持 grid 或 pack
        self._container_cache = {}
        self.paned_window = None  # 用于主区域的可调整大小窗格
        self._setup_main_sections()
        
    def _setup_main_sections(self):
        """创建基础布局区域"""
        # 顶部工具栏区域
        self.add_section("toolbar_section", tk.Frame(self.root), "top")
        
        # 底部状态栏区域
        self.add_section("statusbar_section", tk.Frame(self.root), "bottom")
        
        # 左侧侧边栏区域
        self.add_section("sidebar_section", tk.Frame(self.root), "left")
        
        # 右侧侧边栏区域
        self.add_section("sidebar_section", tk.Frame(self.root), "right")
        
        # 创建主内容区域的可调整窗格
        self._create_main_paned_window()
    
    def _create_main_paned_window(self):
        """创建主内容区域的可调整窗格"""
        # 创建水平分隔窗格
        self.paned_window = tk.PanedWindow(
            self.root, 
            orient=tk.HORIZONTAL,
            sashrelief=tk.RAISED,
            sashwidth=3,
            showhandle=True
        )
        # 将窗格放在主区域位置
        self.paned_window.grid(row=1, column=1, columnspan=2, sticky="nsew")

        # 创建左右侧渲染区域
        main_left_frame = tk.Frame(self.paned_window)
        main_right_frame = tk.Frame(self.paned_window)
        
        # 添加到窗格中
        self.paned_window.add(main_left_frame, stretch="always", minsize=200)
        self.paned_window.add(main_right_frame, stretch="always", minsize=200)
        
        # 添加到sections中
        self.add_section("main_section", main_left_frame, "main_left")
        self.add_section("render_section", main_right_frame, "main_right")
    
    def add_section(self, name: str, container: tk.Widget, anchor: str):
        """添加新的布局区域"""
        section = LayoutSection(name, container, anchor)
        self.sections[name] = section
        self._arrange_all_sections()
        return section
    
    def _arrange_all_sections(self):
        """重新排列所有布局区域"""
        # 清除当前布局（除了paned_window）
        for child in self.root.winfo_children():
            if child != self.paned_window:
                child.grid_forget()
                child.pack_forget()
        
        # 网格布局引擎
        self._arrange_with_grid()
    
    def _arrange_with_grid(self):
        """使用网格布局引擎排列各区域"""
        # 配置网格权重
        self.root.grid_rowconfigure(0, weight=0, minsize=30)   # 顶部区域行 - 固定大小
        self.root.grid_rowconfigure(1, weight=1)  # 主区域行 - 弹性
        self.root.grid_rowconfigure(2, weight=0, minsize=25)    # 底部区域行 - 固定大小
        self.root.grid_columnconfigure(0, weight=0, minsize=50)  # 左侧边栏列 - 固定最小大小
        self.root.grid_columnconfigure(1, weight=1)  # 主区域左列 - 弹性
        self.root.grid_columnconfigure(2, weight=1)  # 主区域右列 - 弹性
        self.root.grid_columnconfigure(3, weight=0, minsize=50)  # 右侧边栏列 - 固定最小大小
        
        # 排列各个区域
        for section in self.sections.values():
            if not section.visible: 
                continue
            
            if section.anchor == "top":
                section.container.grid(row=0, column=0, columnspan=4, sticky="nsew")
            elif section.anchor == "bottom":
                section.container.grid(row=2, column=0, columnspan=4, sticky="nsew")
            elif section.anchor == "left":
                section.container.grid(row=1, column=0, sticky="nsew")
            elif section.anchor == "right":
                section.container.grid(row=1, column=3, sticky="nsew")
    
    def toggle_render_area(self, visible: bool): # TODO: 是否要合并进hide_section() 
        if visible:
            self.sections["render_section"].visible = True
            self.paned_window.add(self.sections["render_section"].container, stretch="always", minsize=200)
        else:
            self.sections["render_section"].visible = False
            self.paned_window.forget(self.sections["render_section"].container)

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