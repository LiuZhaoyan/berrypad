import tkinter as tk

from core.component_basic import ComponentBasic

class ComponentStatus(ComponentBasic):
    """底部状态栏组件"""
    def __init__(self, manager):
        super().__init__(name="component_status", manager=manager)
        self.status_frame = None
        self.status_labels = {}
        
        self._init_statusbar()
        self._bind_events()
    
    def _init_statusbar(self) -> None:
        """初始化状态栏"""
        container = self.manager.layout_manager.get_container("statusbar_bottom")
        # 创建状态栏
        if container:
            self.status_frame = tk.Frame(container, relief=tk.SUNKEN, bd=1)
            self.status_frame.pack(fill=tk.X, padx=2, pady=1)
            
            # 创建默认状态标签
            self._create_status_labels()
    
    def _create_status_labels(self) -> None:
        """创建状态标签"""
        # 左侧状态信息
        self.status_labels['main'] = tk.Label(
            self.status_frame, 
            text="就绪", 
            anchor=tk.W,
            padx=5
        )
        self.status_labels['main'].pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # 右侧状态信息
        self.status_labels['position'] = tk.Label(
            self.status_frame, 
            text="行 1, 列 1", 
            anchor=tk.E,
            padx=5
        )
        self.status_labels['position'].pack(side=tk.RIGHT)
        
        self.status_labels['encoding'] = tk.Label(
            self.status_frame,
            text="UTF-8",
            anchor=tk.E,
            padx=5
        )
        self.status_labels['encoding'].pack(side=tk.RIGHT)
    
    def _bind_events(self) -> None:
        """绑定事件"""
        self.manager.subscribe("status.update", self._on_status_update)
        self.manager.subscribe("editor.cursor_position", self._on_cursor_position)
        self.manager.subscribe("file.encoding_changed", self._on_encoding_changed)
    
    def _on_status_update(self, message: str) -> None:
        """更新主状态信息"""
        if 'main' in self.status_labels:
            self.status_labels['main'].config(text=message)
    
    def _on_cursor_position(self, line: int, column: int) -> None:
        """更新光标位置信息"""
        if 'position' in self.status_labels:
            self.status_labels['position'].config(text=f"行 {line}, 列 {column}")
    
    def _on_encoding_changed(self, encoding: str) -> None:
        """更新编码信息"""
        if 'encoding' in self.status_labels:
            self.status_labels['encoding'].config(text=encoding)
    
    def set_status(self, message: str) -> None:
        """设置状态信息"""
        self.manager.publish("status.update", message=message)
    
    def set_cursor_position(self, line: int, column: int) -> None:
        """设置光标位置"""
        self.manager.publish("editor.cursor_position", line=line, column=column)
    
    def set_encoding(self, encoding: str) -> None:
        """设置编码信息"""
        self.manager.publish("file.encoding_changed", encoding=encoding)