import tkinter as tk
from tkinter import filedialog, ttk
import logging
from components.components import ComponentManager, ComponentFile, ComponentTextArea, ComponentRenderArea, ComponentNotebook
from layout import LayoutManager
# 配置日志系统
def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG, # 设置最低日志级别为 DEBUG
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', # 日志格式
        handlers=[
            # logging.FileHandler("app.log"), # 输出到文件
            logging.StreamHandler() # 输出到控制台
        ]
    )
logger = logging.getLogger(__name__)

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
    editor = TextEditor()
    editor.component_render_area.create_render_area()
    editor.component_notebook.add_tab("Welcome")
    editor.run()
