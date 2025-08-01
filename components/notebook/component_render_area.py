import markdown
from tkinterweb import HtmlFrame
import tkinter as tk

from core.component_basic import ComponentBasic
from core.component_manager import ComponentManager


class ComponentRenderArea(ComponentBasic):
    """Markdown 渲染区域组件"""
    def __init__(self, manager: ComponentManager):
        super().__init__(
            name="render_area",
            manager=manager
        )
        self.render_html = None  # 全局一个HTML组件
        self.in_sync = False     # 防止滚动循环的标志位

        self._init_render_area()

    def _init_render_area(self):
        """初始化渲染区域"""
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