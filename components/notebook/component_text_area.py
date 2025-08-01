from core.component_basic import ComponentBasic
from core.component_manager import ComponentManager
import tkinter as tk

class ComponentTextArea(ComponentBasic):
    """文本区域组件"""
    def __init__(self, manager: ComponentManager):
        super().__init__(
            name="text_area", 
            manager=manager
        )

        self.text_area = None  # 当前标签页的文本组件
        self.current_tab = None  # 当前活动标签页的 frame

        self._init_text_area()

    def _init_text_area(self):
        """初始化文本区域组件"""
        # 订阅事件
        self.manager.subscribe("new_tab_generated", self.create_text_area)
        self.manager.subscribe("font_changed", self.update_font)
        self.manager.subscribe("tab_switched", self.on_tab_switched)

    def create_text_area(self, tab_name: str):
        """为标签页创建文本区域"""
        tab_frame = self.manager.get_component("component_notebook").get_tab_by_name(tab_name)
        
        scrollbar = tk.Scrollbar(tab_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        if not self.check_direct_text_child(tab_frame):
            text_area = tk.Text(
                tab_frame,
                wrap=tk.WORD,
                padx=10,
                pady=10,
                yscrollcommand=scrollbar.set
            )
            text_area.pack(fill=tk.BOTH, expand=True)
            # 绑定文本修改事件
            text_area.bind('<<Modified>>', self.on_text_modified)
        else:
            self.text_area.delete("1.0", tk.END)  # 清空旧内容

        self.text_area = self.check_direct_text_child(tab_frame)
        scrollbar.config(command=self.text_area.yview)
        # tk绑定事件
        self.text_area.bind("<MouseWheel>", self.on_text_scroll)
        
    def on_text_scroll(self, event):
        """处理文本区域滚动事件"""
        if self.text_area:
            # 获取当前滚动位置
            fraction = self.text_area.yview()[0]
            # 向外部发布滚动事件
            self.manager.publish("text_scrolled", fraction=fraction)

    def on_text_modified(self, event=None):
        """处理文本修改事件（触发渲染更新）"""
        # 避免重复触发<<Modified>> 事件会在内容变化后自动标记为已修改
        self.text_area.edit_modified(False)
        
        content = self.text_area.get("1.0", tk.END).strip()
        # 更新缓存
        notebook_component = self.manager.get_component("component_notebook")
        current_tab_name = notebook_component.get_current_tab_name()
        if current_tab_name:
            notebook_component.tab_content_cache[current_tab_name] = content

        # 发布事件通知渲染区域更新
        self.manager.publish("text_updated", content=content)
    
    def on_tab_switched(self, new_tab_frame: tk.Frame):
        """处理标签页切换事件"""
        self.current_tab = new_tab_frame
        if self.check_direct_text_child(new_tab_frame):
            self.text_area = self.check_direct_text_child(new_tab_frame)
        # logger.info(f"Switched to text_area: {self.text_area}")
    
    def update_font(self, family: str, size: int):
        """更新所有标签页的字体"""
        notebook = self.manager.get_component("component_notebook").widget
        for tab_id in notebook.tabs():
            tab_frame = notebook.nametowidget(tab_id)
            if self.check_direct_text_child(tab_frame):
                self.check_direct_text_child(tab_frame).config(font=(family, size))
