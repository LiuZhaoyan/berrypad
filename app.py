import tkinter as tk
from components.font.font_manager import FontManager
from components.menu_actions.paragraph_actions import CodeBlockAction, HeadingAction, OrderedListAction, QuoteAction, UnorderedListAction
from components.menu_actions.theme_actions import FontSelectAction, FontSizeDecreaseAction, FontSizeIncreaseAction, FontSizeResetAction
from components.menu_actions.view_actions import ToggleRenderModeAction
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
from components.menu_actions.format_actions import StrikeAction, StrongAction, EmphasisAction, UnderlineAction, CodeAction

class MarkdownEditorApp:
    """主应用类"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Berrypad")
        self.root.geometry("1200x700")
        self.root.iconbitmap("berrypad.ico")
        # 初始化核心组件
        self.layout_manager = LayoutManager(self.root)
        self.component_manager = ComponentManager(self.root, self.layout_manager)
        self.menu_manager = MenuManager(self.component_manager)
        self.font_manager = FontManager(self.component_manager)
        
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
        component_status = ComponentStatus(self.component_manager, self.layout_manager, self.font_manager)
        
    
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
            StrongAction("strong_action", self.component_manager),
            EmphasisAction("emphasis_action", self.component_manager),
            UnderlineAction("underline_action", self.component_manager),
            CodeAction("code_action", self.component_manager),
            StrikeAction("strike_action", self.component_manager),
            ToggleRenderModeAction("toggle_render_mode_action", self.component_manager),
            HeadingAction("heading_action", self.component_manager),
            QuoteAction("quote_action", self.component_manager),
            UnorderedListAction("unordered_list_action", self.component_manager),
            OrderedListAction("ordered_list_action", self.component_manager),
            CodeBlockAction("code_block_action", self.component_manager),
            FontSizeIncreaseAction("font_size_increase_action", self.component_manager),
            FontSizeDecreaseAction("font_size_decrease_action", self.component_manager),
            FontSizeResetAction("font_size_reset_action", self.component_manager),
        ]
        # 为常用字体创建动作组件
        common_fonts = ["微软雅黑", "宋体", "黑体", "Arial", "Times New Roman", "Courier New"]
        for font_name in common_fonts:
            # 创建安全的组件名称
            safe_name = font_name.replace(" ", "_").replace("-", "_")
            action = FontSelectAction(f"font_{safe_name}_action", self.component_manager, font_name)
            actions.append(action)
    
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

        # 标题菜单
        self.menu_manager.register_menu(
            menu_name="paragraph_menu",
            button_text="标题",
            menu_items=[
                ("标题 1", self.component_manager.get_component("heading_action").execute_1, "<Control-Key-1>"),
                ("标题 2", self.component_manager.get_component("heading_action").execute_2, "<Control-Key-2>"),
                ("标题 3", self.component_manager.get_component("heading_action").execute_3, "<Control-Key-3>"),
                ("标题 4", self.component_manager.get_component("heading_action").execute_4, "<Control-Key-4>"),
                ("标题 5", self.component_manager.get_component("heading_action").execute_5, "<Control-Key-5>"),
                ("标题 6", self.component_manager.get_component("heading_action").execute_6, "<Control-Key-6>"),
                ("---", None, None),  # 分隔线
                ("引用", self.component_manager.get_component("quote_action").execute, "<Control-q>"),
                ("无序列表", self.component_manager.get_component("unordered_list_action").execute, "<Control-bracketleft>"),
                ("有序列表", self.component_manager.get_component("ordered_list_action").execute, "<Control-bracketright>"),
                ("代码块", self.component_manager.get_component("code_block_action").execute, "<Control-Shift-K>")
            ],
            menu_shortcut=""
        )

        # 格式菜单
        self.menu_manager.register_menu(
            menu_name="format_menu",
            button_text="格式",
            menu_items=[
                ("加粗", self.component_manager.get_component("strong_action").execute, "<Control-b>"),
                ("斜体", self.component_manager.get_component("emphasis_action").execute, "<Control-l>"),
                ("下划线", self.component_manager.get_component("underline_action").execute, "<Control-u>"),
                ("代码行", self.component_manager.get_component("code_action").execute, "<Control-k>"),
                ("删除线", self.component_manager.get_component("strike_action").execute, "<Control-d>")
            ],
            menu_shortcut=""
        )

        # 视图菜单
        self.menu_manager.register_menu(
            menu_name="view_menu",
            button_text="视图",
            menu_items=[
                ("退出渲染", self.component_manager.get_component("toggle_render_mode_action").execute, "<Control-/>")
            ],
            menu_shortcut="<Control-V>"
        )

        # 主题菜单
        # 先创建字体选择项列表
        font_menu_items = [
            ("增大字体", self.component_manager.get_component("font_size_increase_action").execute, "<Control-plus>"),
            ("减小字体", self.component_manager.get_component("font_size_decrease_action").execute, "<Control-minus>"),
            ("重置字体", self.component_manager.get_component("font_size_reset_action").execute, "<Control-0>"),
            ("---", None, None),  # 分隔线
        ]
        
        # 添加常用字体选项
        common_fonts = ["微软雅黑", "宋体", "黑体", "Arial", "Times New Roman", "Courier New"]
        for font_name in common_fonts:
            safe_name = font_name.replace(" ", "_").replace("-", "_")
            font_menu_items.append((
                font_name, 
                self.component_manager.get_component(f"font_{safe_name}_action").execute, 
                None
            ))
        
        self.menu_manager.register_menu(
            menu_name="theme_menu",
            button_text="主题",
            menu_items=font_menu_items,
            menu_shortcut="<Control-T>"
        )
    
    def _register_editor(self) -> None:
        """注册编辑器相关组件"""
        # 注册Notebook组件
        notebook_component = ComponentNotebook(self.component_manager)
        
        # 注册文本区域组件
        text_area_component = ComponentTextArea(self.component_manager, self.font_manager)
        
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