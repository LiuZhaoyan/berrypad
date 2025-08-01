import tkinter as tk
from tkinter import ttk

from core.component_basic import ComponentBasic


class ComponentNotebook(ComponentBasic):
    """主容器-集成Notebook多标签管理"""
    def __init__(self, manager):
        super().__init__(
            name="component_notebook",
            manager=manager
            )
        self.frame = self.get_container()
        self.notebook = None
        self._tabs = {} # 存储标签页的字典，{标签名, Frame}
        self.tab_content_cache = {}  # 缓存各标签页的文本内容，{标签名, 文本内容}
    
        self._init_notebook()

    def _init_notebook(self):
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill='both', expand=True)
        self.notebook.bind(
            '<<NotebookTabChanged>>',
            lambda event: self.manager.publish("tab_switched", new_tab_frame=self.notebook.nametowidget(self.notebook.select()))
        )
    
    def add_tab(self, tab_name: str) -> tk.Frame:
        """添加新标签页"""
        frame = tk.Frame(self.notebook)
        self.notebook.add(frame, text=tab_name)
        self._tabs[tab_name] = frame

        self.manager.publish("new_tab_generated", tab_name=tab_name)
        self.switch_tab_by_name(tab_name)  # 切换到新标签页

        return frame

    def set_tab_name(self, old_name: str, new_name: str) -> None:
        """设置标签页名称"""
        if old_name in self._tabs.keys():
            frame = self._tabs[old_name]
            tab_id = self.get_tab_id_by_name(old_name)
            self.notebook.tab(tab_id, text=new_name)
            del self._tabs[old_name]
            self._tabs[new_name] = frame
            # 更新缓存中的标签名
            if old_name in self.tab_content_cache.keys():
                self.tab_content_cache[new_name] = self.tab_content_cache.pop(old_name)

    def get_tab_by_name(self, tab_name: str ) -> tk.Frame:
        """根据标签名获取标签页"""
        return self._tabs.get(tab_name, None)
    
    def switch_tab_by_name(self, tab_name: str):
        """切换到指定标签页"""
        for tab_id in self.notebook.tabs():
            # 获取当前标签页的显示文本
            current_text = self.notebook.tab(tab_id, 'text')
            if current_text == tab_name:
                return self.notebook.select(tab_id)
        return None
    
    def get_tab_id_by_name(self, tab_name: str):
        for tab_id in self.notebook.tabs():
            # 获取当前标签页的显示文本
            current_text = self.notebook.tab(tab_id, 'text')
            if current_text == tab_name:
                return tab_id

    def get_current_tab_name(self) -> str:
        """获取当前选中标签页的名称"""
        current_tab_id = self.notebook.select()
        return self.notebook.tab(current_tab_id, 'text')
