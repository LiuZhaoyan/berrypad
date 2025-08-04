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
        self.manager.subscribe("tab_switched", self._on_tab_switched)

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
                yscrollcommand=scrollbar.set,
                undo=True,
                maxundo=50
            )
            text_area.pack(fill=tk.BOTH, expand=True)
            # 绑定文本修改事件
            text_area.bind('<<Modified>>', self._on_text_modified)
             # 绑定键盘快捷键
            self._bind_cursor_events(text_area)
        else:
            self.text_area.delete("1.0", tk.END)  # 清空旧内容

        self.text_area = self.check_direct_text_child(tab_frame)
        scrollbar.config(command=self.text_area.yview)
        # tk绑定事件
        self.text_area.bind("<MouseWheel>", self._on_text_scroll)
        
    def _on_text_scroll(self, event):
        """处理文本区域滚动事件"""
        if self.text_area:
            # 获取当前滚动位置
            fraction = self.text_area.yview()[0]
            # 向外部发布滚动事件
            self.manager.publish("text_scrolled", fraction=fraction)

    def _on_text_modified(self, event=None):
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
    
    def _on_tab_switched(self, new_tab_frame: tk.Frame):
        """处理标签页切换事件"""
        self.current_tab = new_tab_frame
        if self.check_direct_text_child(new_tab_frame):
            self.text_area = self.check_direct_text_child(new_tab_frame)
        # logger.info(f"Switched to text_area: {self.text_area}")
    
    def _bind_cursor_events(self, text_area):
        """绑定光标移动相关事件"""
        # 键盘输入事件
        text_area.bind('<KeyRelease>', self._on_text_cursor_moved)
        # 鼠标点击事件
        text_area.bind('<Button-1>', self._on_text_cursor_moved)
        text_area.bind('<Button-3>', self._on_text_cursor_moved)
        # 方向键事件
        text_area.bind('<KeyPress-Up>', self._on_text_cursor_moved)
        text_area.bind('<KeyPress-Down>', self._on_text_cursor_moved)
        text_area.bind('<KeyPress-Left>', self._on_text_cursor_moved)
        text_area.bind('<KeyPress-Right>', self._on_text_cursor_moved)
        # Home/End键事件
        text_area.bind('<KeyPress-Home>', self._on_text_cursor_moved)
        text_area.bind('<KeyPress-End>', self._on_text_cursor_moved)
        # PageUp/PageDown事件
        text_area.bind('<KeyPress-Prior>', self._on_text_cursor_moved)
        text_area.bind('<KeyPress-Next>', self._on_text_cursor_moved)

    def _on_text_cursor_moved(self, event=None):
        """处理文本光标移动事件 - 实时获取并广播光标位置"""
        # 获取触发事件的文本组件
        text_widget = event.widget if event else self._get_active_text_area()
        if text_widget:
            try:
                # 获取光标位置
                cursor_pos = text_widget.index(tk.INSERT)
                
                # 解析行号和列号（注意：Tkinter行号从1开始，列号从0开始）
                line, column = cursor_pos.split('.')
                line = int(line)
                col = int(column) + 1
                
                # 发布光标位置事件
                self.manager.publish("text_cursor_moved", line=line, column=col)
                
            except Exception as e:
                print(f"获取光标位置时出错: {e}")

    def update_font(self, family: str, size: int):
        """更新所有标签页的字体"""
        notebook = self.manager.get_component("component_notebook").widget
        for tab_id in notebook.tabs():
            tab_frame = notebook.nametowidget(tab_id)
            if self.check_direct_text_child(tab_frame):
                self.check_direct_text_child(tab_frame).config(font=(family, size))

    @staticmethod
    def check_direct_text_child(frame) -> tk.Widget:
        """检查是否有直接的文本子组件"""
        for child in frame.winfo_children():
            if isinstance(child, tk.Text):
                return child
        return None
