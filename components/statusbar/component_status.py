import tkinter as tk
from core.component_basic import ComponentBasic

class ComponentStatus(ComponentBasic):
    """底部状态栏组件"""
    def __init__(self, manager, layout_manager):
        super().__init__(name="component_status", manager=manager)
        self.layout_manager = layout_manager
        self.status_frame = None
        self.status_labels = {}
        self.toggle_button = None
        self.render_visible = True  # 跟踪渲染区域是否可见
        
        self._init_statusbar()
        self._bind_events()
    
    def _init_statusbar(self) -> None:
        """初始化状态栏"""
        container = self.layout_manager.get_container("statusbar_bottom")
        # 创建状态栏
        if container:
            self.status_frame = tk.Frame(container, relief=tk.SUNKEN, bd=1)
            self.status_frame.pack(fill=tk.X, padx=2, pady=1)
            
            # 创建切换按钮
            self._create_toggle_button()
            
            # 创建默认状态标签
            self._create_status_labels()
    
    def _bind_events(self) -> None:
        """绑定事件"""
        self.manager.subscribe("status_updated", self._on_status_updated)
        self.manager.subscribe("file.encoding_changed", self._on_encoding_changed)
        self.manager.subscribe("text_cursor_moved", self._on_text_cursor_moved)

        self.manager.subscribe("view.toggle_render_mode", self._on_toggle_click)
     
    def _create_toggle_button(self) -> None:
        """创建圆形切换按钮"""
        # 创建按钮容器，用于居中圆形按钮
        button_container = tk.Frame(self.status_frame)
        button_container.pack(side=tk.LEFT, padx=5, pady=2)
        
        # 创建圆形按钮
        self.toggle_button = tk.Canvas(
            button_container,
            width=20,
            height=20,
            highlightthickness=0,
            relief=tk.FLAT
        )
        self.toggle_button.pack()
        
        # 绘制圆形按钮（初始状态：显示渲染区域）
        button_id = self.toggle_button.create_oval(3, 3, 15.5, 15.5, fill="#FFFFFF", outline="#393838", width=2)

        # 绑定事件
        self.toggle_button.bind("<Button-1>", lambda e: self._on_toggle_click())
        self.toggle_button.bind("<Enter>", lambda e: self._on_button_hover(True, button_id))
        self.toggle_button.bind("<Leave>", lambda e: self._on_button_hover(False, button_id))
    
    def _on_button_hover(self, enter: bool, button_id: int) -> None:
        """按钮悬停效果"""
        if enter:
            self.toggle_button.config(cursor="hand2")
            self.toggle_button.itemconfig(button_id, fill="#9E9E9E")
        else:
            self.toggle_button.config(cursor="")
            self.toggle_button.itemconfig(button_id, fill="#FFFFFF")
    
    def _on_toggle_click(self) -> None:
        """切换按钮点击事件"""
        self.render_visible = not self.render_visible
        # 根据状态绘制不同颜色的圆
        if self.render_visible:
            self.toggle_button.itemconfig("all", fill="#9E9E9E")  # 白色：显示渲染区域
        else:
            self.toggle_button.itemconfig("all", fill="#FFFFFF")  # 白色：显示渲染区域
        
        # 切换渲染区域显示状态
        self._toggle_render_area()
        
        # 更新状态提示
        status_text = "双栏显示模式" if self.render_visible else "单栏编辑模式"
        self.set_status(status_text)
    
    def _toggle_render_area(self) -> None:
        """切换渲染区域显示/隐藏"""
        if self.render_visible:
            # 显示渲染区域，恢复双栏布局
            self.layout_manager.show_section("render_section")
            self.layout_manager.show_section("main_area")
            
            # 调整主区域权重
            self._adjust_layout_weights(show_render=True)
        else:
            # 隐藏渲染区域，编辑区域填充整个空间
            self.layout_manager.hide_section("render_section")
            
            # 调整主区域权重，让编辑区域占满空间
            self._adjust_layout_weights(show_render=False)
    
    def _adjust_layout_weights(self, show_render: bool) -> None:
        """调整布局权重"""
        try:
            if show_render:
                # 双栏模式：主区域和渲染区域各占一半
                self.layout_manager.root.grid_columnconfigure(1, weight=100)  # 主区域
                self.layout_manager.root.grid_columnconfigure(2, weight=100)  # 渲染区域
            else:
                # 单栏模式：主区域占满空间
                self.layout_manager.root.grid_columnconfigure(1, weight=100)  # 主区域
                self.layout_manager.root.grid_columnconfigure(2, weight=0)  # 渲染区域
        except Exception as e:
            print(f"调整布局权重时出错: {e}")
    
    def _create_status_labels(self) -> None:
        """创建状态标签"""
        # 左侧状态信息（在按钮右侧）
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

    def _on_status_updated(self, message: str) -> None:
        """更新主状态信息"""
        if 'main' in self.status_labels:
            self.status_labels['main'].config(text=message)
    
    def _on_text_cursor_moved(self, line: int, column: int) -> None:
        """处理文本光标移动事件"""
        self.set_cursor_position(line, column)
    
    def _on_encoding_changed(self, encoding: str) -> None:
        """更新编码信息"""
        if 'encoding' in self.status_labels:
            self.status_labels['encoding'].config(text=encoding)
    
    def set_status(self, message: str) -> None:
        """设置状态信息"""
        self.manager.publish("status_updated", message=message)
    
    def set_cursor_position(self, line: int, column: int) -> None:
        """设置光标位置"""
        if 'position' in self.status_labels:
            self.status_labels['position'].config(text=f"行 {line}, 列 {column}")
    
    def set_encoding(self, encoding: str) -> None:
        """设置编码信息"""
        self.manager.publish("file.encoding_changed", encoding=encoding)
    
    def is_render_visible(self) -> bool:
        """获取渲染区域是否可见"""
        return self.render_visible