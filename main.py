
# 配置日志系统
import logging
import sys
from logging import StreamHandler

def configure_logging(level: int = logging.INFO) -> None:
    """
    全局配置日志输出到终端（不生成文件）
    
    Args:
        level: 日志级别（默认INFO，可选DEBUG/INFO/WARNING/ERROR/CRITICAL）
    """
    # 避免重复配置（如果已经配置过则跳过）
    if logging.root.handlers:
        return

    # 定义日志格式（可根据需求调整）
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # 配置终端输出（使用StreamHandler指向标准输出）
    console_handler = StreamHandler(sys.stdout)
    console_handler.setLevel(level)  # 处理器级别（过滤低于此级别的日志）
    
    # 设置日志格式
    formatter = logging.Formatter(log_format)
    console_handler.setFormatter(formatter)
    
    # 配置根日志器
    root_logger = logging.getLogger()
    root_logger.setLevel(level)  # 根日志器级别（全局最低级别）
    root_logger.addHandler(console_handler)
    
logger = logging.getLogger(__name__)

import tkinter as tk
from tkinter import filedialog, ttk
from components.components import ComponentManager, ComponentFile, ComponentTextArea, ComponentRenderArea, ComponentNotebook
from layout import LayoutManager

# --------------------------
# 主程序协调各组件
# --------------------------

class TextEditor:
    def __init__(self, root_title="berrypad"):
        self.root = tk.Tk()
        self.root.title(root_title)
        self.root.geometry("1000x700")
        
        # 初始化布局管理器
        self.layout_manager = LayoutManager(self.root)

        # 组件管理器
        self.component_manager = ComponentManager(self.root, self.layout_manager)
        
        # 主容器
        self.component_notebook = ComponentNotebook(self.component_manager)

        # 文本区域组件
        self.component_text_area = ComponentTextArea(self.component_manager)

        # 渲染区域组件
        self.component_render_area = ComponentRenderArea(self.component_manager)
        # 初始化核心组件
        # self._init_components()

    def _init_components(self):
        """按顺序初始化各功能组件"""
        # 1. 主容器组件
        # MainContainer(self.component_manager)
        
        # 2. 文本区域组件
        ComponentTextArea(self.component_manager)
        
        # 3. 字体管理组件
        # ComponentFont(self.component_manager)
        
        # 4. 文件管理组件
        # ComponentFile(self.component_manager)
            
    def run(self):
        self.root.mainloop()

# 启动程序
if __name__ == "__main__":
    configure_logging(level=logging.DEBUG)
    editor = TextEditor()
    editor.component_render_area.create_render_area()
    editor.component_notebook.add_tab("Welcome")
    editor.run()
