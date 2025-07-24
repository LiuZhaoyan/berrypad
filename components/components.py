import logging
logger = logging.getLogger(__name__)

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from components.component_basic import ComponentBasic, ComponentManager
import markdown
from tkinterweb import HtmlFrame

# --------------------------
# 功能组件模块化实现
# --------------------------

class ComponentNotebook(ComponentBasic):
    """主容器-集成Notebook多标签管理"""
    def __init__(self, manager):
        super().__init__(
            name="component_notebook",
            manager=manager
            )
        self.frame = self.get_container()
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill='both', expand=True)
        self.notebook.bind(
            '<<NotebookTabChanged>>',
            lambda event: self.manager.publish("tab_switched", new_tab_frame=self.notebook.nametowidget(self.notebook.select()))
        )
        self._tabs = {} # 存储标签页的字典，键为标签名，值为对应的Frame
        self.tab_content_cache = {}  # 缓存各标签页的文本内容，键为标签名，值为文本内容
    
    def add_tab(self, tab_name: str) -> tk.Frame:
        """添加新标签页"""
        frame = tk.Frame(self.notebook)
        self.notebook.add(frame, text=tab_name)
        self._tabs[tab_name] = frame

        self.manager.publish("new_tab_generated", tab_name=tab_name)
        self.switch_tab_by_name(tab_name)  # 切换到新标签页

        return frame

    def get_tab_by_name(self, tab_name: str):
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
    
    def get_current_tab_name(self):
        """获取当前选中标签页的名称"""
        current_tab_id = self.notebook.select()
        return self.notebook.tab(current_tab_id, 'text')

class ComponentFont:
    """字体管理组件"""
    def __init__(self, manager: ComponentManager):
        self.manager = manager
        self.font_family = "Helvetica"
        self.font_size = 12
        
        # 注册组件
        manager.register_component(ComponentBasic(
            name="font_control",
            widget=None,
            dependencies=["component_notebook"],
            init_hook=self.setup_font_controls
        ))
    
    def setup_font_controls(self):
        """设置字体控制组件"""
        toolbar = tk.Frame(self.manager.root)
        toolbar.pack(fill=tk.X)
        
        # 字体选择
        font_var = tk.StringVar(value=self.font_family)
        font_menu = ttk.Combobox(toolbar, textvariable=font_var, width=15)
        font_menu["values"] = ["Helvetica", "Arial", "Times", "Courier", "Verdana"]
        font_menu.bind("<<ComboboxSelected>>", self._on_font_change)
        font_menu.pack(side=tk.LEFT, padx=5)
        
        # 字号选择
        size_var = tk.IntVar(value=self.font_size)
        size_spin = tk.Spinbox(toolbar, from_=8, to=72, textvariable=size_var, width=5)
        size_spin.bind("<Return>", self._on_size_change)
        size_spin.bind("<FocusOut>", self._on_size_change)
        size_spin.pack(side=tk.LEFT, padx=5)
        
        # 注册订阅事件
        self.manager.subscribe("text_widget_created", self.apply_current_font)
        
    def _on_font_change(self, event):
        self.font_family = event.widget.get()
        self.manager.publish("font_changed", family=self.font_family, size=self.font_size)
        logging.info(f"字体更改为: {self.font_family}")
    
    def _on_size_change(self, event):
        try:
            self.font_size = int(event.widget.get())
            self.manager.publish("font_changed", family=self.font_family, size=self.font_size)
            logging.info(f"字号更改为: {self.font_size}")
        except ValueError:
            pass
    
    def apply_current_font(self, text_widget: tk.Text):
        text_widget.config(font=(self.font_family, self.font_size))

class ComponentFile:
    """文件管理组件"""
    def __init__(self, manager: ComponentManager):
        self.manager = manager
        
        # 注册组件
        manager.register_component(ComponentBasic(
            name="file_control",
            widget=None,
            dependencies=["component_notebook"],
            init_hook=self.setup_file_controls
        ))
        
        # 文档状态跟踪
        self.current_file = {}
    
    def setup_file_controls(self):
        """设置文件控制组件"""
        toolbar = tk.Frame(self.manager.root)
        toolbar.pack(fill=tk.X)
        
        # 新建按钮
        new_btn = tk.Button(toolbar, text="新建", command=self.new_file)
        new_btn.pack(side=tk.LEFT, padx=5)
        
        # 打开按钮
        open_btn = tk.Button(toolbar, text="打开", command=self.open_file)
        open_btn.pack(side=tk.LEFT, padx=5)
        
        # 保存按钮
        save_btn = tk.Button(toolbar, text="保存", command=self.save_file)
        save_btn.pack(side=tk.LEFT, padx=5)
        
        # 注册事件
        self.manager.subscribe("new_tab", self.track_new_tab)
    
    def track_new_tab(self, tab_name: str):
        """跟踪新标签页状态"""
        self.current_file[tab_name] = {"path": None, "unsaved": False}
    
    def new_file(self):
        """新建文件"""
        container = self.manager.get_component("component_notebook").widget
        tab_name = f"文档{len(container.tabs()) + 1}"
        container.add_tab(tab_name)
        logging.info(f"已新建文档: {tab_name}")
    
    def open_file(self):
        """打开文件"""
        file_path = filedialog.askopenfilename(
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    container = self.manager.get_component("component_notebook").widget
                    tab_name = f"{file_path.split('/')[-1]}"
                    frame = container.add_tab(tab_name)
                    
                    # 获取当前标签页的文本框
                    text_widget = frame.winfo_children()[0]
                    text_widget.insert("1.0", content)
                    
                    self.current_file[tab_name] = {"path": file_path, "unsaved": False}
                    logging.info(f"已打开文件: {file_path}")
            except Exception as e:
                logging.error(f"打开文件失败: {str(e)}")
    
    def save_file(self):
        """保存文件"""
        # 获取当前激活的标签页
        container = self.manager.get_component("component_notebook").widget
        current_tab = container.select()
        tab_name = container.tab(current_tab, "text")
        
        # 获取当前标签页的文本框
        text_widget = container.nametowidget(current_tab).winfo_children()[0]
        content = text_widget.get("1.0", "end-1c")
        
        # 获取文件信息
        file_info = self.current_file.get(tab_name, {"path": None})
        file_path = file_info["path"]
        
        # 如果没有路径则打开保存对话框
        if not file_path:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
            )
            if not file_path:
                return
            
            # 更新标签页名称
            tab_name = file_path.split("/")[-1]
            container.tab(current_tab, text=tab_name)
        
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
                self.current_file[tab_name] = {"path": file_path, "unsaved": False}
                logging.info(f"已保存文件: {file_path}")
        except Exception as e:
            logging.error(f"保存文件失败: {str(e)}")

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

class ComponentTextArea(ComponentBasic):
    """文本区域组件"""
    def __init__(self, manager: ComponentManager):
        super().__init__(
            name="text_area", 
            manager=manager
        )

        self.text_area = None  # 当前标签页的文本组件
        self.current_tab = None  # 当前活动标签页的 frame

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

class ComponentRenderArea(ComponentBasic):
    """Markdown 渲染区域组件"""
    def __init__(self, manager: ComponentManager):
        super().__init__(
            name="render_area",
            manager=manager
        )
        self.render_html = None  # 全局一个HTML组件
        self.in_sync = False     # 防止滚动循环的标志位

        # 订阅事件
        self.manager.subscribe("text_scrolled", self.on_text_scrolled)
        self.manager.subscribe("text_updated", self.render_markdown)
        self.manager.subscribe("tab_switched", self.on_tab_switched_render)
    
    def create_render_area(self):
        """创建 HTML 渲染容器"""
        container = self.get_container()
        # 使用 HtmlFrame 支持 HTML 显示
        self.render_html = HtmlFrame(
            container
        )
        self.render_html.pack(fill=tk.BOTH, expand=True)
    
    def render_markdown(self, content: str):
        """将 Markdown 内容渲染为 HTML 并显示"""
        if not content:
            self.render_html.load_html("<p>暂无内容</p>")  # 空内容提示
            return
        
        try:
            # 将 Markdown 转换为 HTML
            html_content = markdown.markdown(
                content,
                extras=["fenced-code-blocks", "tables"]  # 启用代码块和表格支持
            )
            # 加载 HTML 到渲染组件
            self.render_html.load_html(html_content)
        except Exception as e:
            self.render_html.load_html(f"<p>渲染错误: {str(e)}</p>")
    
    def on_text_scrolled(self, fraction):
        """处理文本区域滚动事件（保持与渲染区域同步）"""
        if self.in_sync or not self.render_html:
            return
        
        self.in_sync = True
        try:
            # 同步垂直滚动位置（HtmlFrame 的滚动范围是 0.0-1.0）
            self.render_html.yview_moveto(fraction)
        finally:
            self.in_sync = False

    def on_tab_switched_render(self, new_tab_frame: tk.Frame):
        """处理标签页切换事件，从缓存中读取内容并渲染"""
        notebook_component = self.manager.get_component("component_notebook")
        current_tab_name = notebook_component.get_current_tab_name()
        if current_tab_name and current_tab_name in notebook_component.tab_content_cache:
            # 从缓存获取内容并渲染
            cached_content = notebook_component.tab_content_cache[current_tab_name]
            self.render_markdown(cached_content)
        else:
            # 新标签页或无缓存，渲染空内容
            self.render_markdown("")


    def get_layout_section(self):
        return "render_section"
