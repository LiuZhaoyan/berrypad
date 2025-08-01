import tkinter as tk
from core.component_manager import ComponentManager
from core.layout_manager import LayoutManager
from components.toolbar.menu_manager import MenuManager
from components.toolbar.component_tool import ComponentTool
from components.statusbar.component_status import ComponentStatus
from components.notebook.component_notebook import ComponentNotebook
from components.notebook.component_text_area import ComponentTextArea
from components.notebook.component_render_area import ComponentRenderArea
from components.editor.component_editor import TextEditor
from components.menu_actions.file_actions import NewFileAction, OpenFileAction, SaveAsFileAction, SaveFileAction
from components.menu_actions.edit_actions import CopyAction, PasteAction, CutAction

class MarkdownEditorApp:
    """主应用类"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Berrypad")
        self.root.geometry("1200x800")
        
        # 初始化核心组件
        self.layout_manager = LayoutManager(self.root)
        self.component_manager = ComponentManager(self.root, self.layout_manager)
        self.menu_manager = MenuManager(self.component_manager)
        
        # 注册基础组件
        self._register_core_components()
        
        # 注册菜单动作组件
        self._register_menu_actions()
        
        # 注册默认菜单
        self._register_default_menus()
        
        # 注册编辑器组件
        self._register_editor()
    
    def _register_core_components(self) -> None:
        """注册核心组件"""
        component_tool = ComponentTool(self.component_manager, self.menu_manager)
        component_status = ComponentStatus(self.component_manager)
        
    
    def _register_menu_actions(self) -> None:
        """注册菜单动作组件"""
        actions = [
            NewFileAction("new_file_action", self.component_manager),
            OpenFileAction("open_file_action", self.component_manager),
            SaveFileAction("save_file_action", self.component_manager),
            SaveAsFileAction("save_as_file_action", self.component_manager),
            CopyAction("copy_action", self.component_manager),
            PasteAction("paste_action", self.component_manager),
            CutAction("cut_action", self.component_manager),
        ]
        
        for action in actions:
            self.component_manager.register_component(action)
    
    def _register_default_menus(self) -> None:
        """注册默认菜单"""
        # 文件菜单
        self.menu_manager.register_menu(
            menu_name="file_menu",
            button_text="文件",
            menu_items=[
                ("新建", self.component_manager.get_component("new_file_action").execute, "<Control-n>"),
                ("打开", self.component_manager.get_component("open_file_action").execute, "<Control-o>"),
                ("保存", self.component_manager.get_component("save_file_action").execute, "<Control-s>"),
                ("另存为", self.component_manager.get_component("save_as_file_action").execute, "<Control-Shift-S>")
            ],
            menu_shortcut="<Control-F>"
        )
        
        # 编辑菜单
        self.menu_manager.register_menu(
            menu_name="edit_menu",
            button_text="编辑",
            menu_items=[
                ("复制", self.component_manager.get_component("copy_action").execute, "<Control-c>"),
                ("粘贴", self.component_manager.get_component("paste_action").execute, "<Control-v>"),
                ("剪切", self.component_manager.get_component("cut_action").execute, "<Control-x>")
            ],
            menu_shortcut="<Control-E>"
        )
    
    def _register_editor(self) -> None:
        """注册编辑器相关组件"""
        # 注册Notebook组件
        notebook_component = ComponentNotebook(self.component_manager)
        
        # 注册文本区域组件
        text_area_component = ComponentTextArea(self.component_manager)
        
        # 注册渲染区域组件
        render_area_component = ComponentRenderArea(self.component_manager)
        
        # 注册主编辑器组件
        text_editor = TextEditor(self.component_manager)
        
        # 将组件放置到正确的布局区域

        render_area_component.create_render_area()  # 创建渲染区域
        
        # 创建初始标签页
        notebook_component.add_tab("Welcome")
    
    def run(self) -> None:
        """运行应用"""
        self.root.mainloop()