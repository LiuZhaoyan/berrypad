import tkinter as tk
from tkinter import filedialog
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# --------------------------
# 模块1：字体管理（独立功能模块）
# --------------------------
class FontManager:
    def __init__(self, text_widget):
        self.text_widget = text_widget  # 文本框引用
        self.available_fonts = {        # 可扩展的字体配置
            "Helvetica": {"var": tk.IntVar(), "display_name": "Helvetica"},
            "Courier": {"var": tk.IntVar(), "display_name": "Courier"}
        }
    
    def create_font_menu(self, parent_widget):
        """为指定父组件创建字体选择菜单"""
        menu = tk.Menu(parent_widget, tearoff=0)
        
        # 动态生成菜单项（支持后续扩展）
        for font_name, config in self.available_fonts.items():
            menu.add_checkbutton(
                label=config["display_name"],
                variable=config["var"],
                command=lambda fn=font_name: self.set_font(fn)  # 传递字体名称
            )
            if font_name == "Helvetica":
                config["var"].set(1)  # 默认选中第一个字体
        return menu
    
    def set_font(self,fn):
        """统一设置字体"""
        if fn in self.available_fonts and self.text_widget:
            for name in self.available_fonts:
                self.available_fonts[name]["var"].set(1 if name == fn else 0)
            self.text_widget.config(font=fn)
            logging.info(f"Font set to {fn}")
        else:
            logging.error(f"Font {fn} not found in available fonts.")
            raise ValueError(f"Font {fn} not found in available fonts.")

# --------------------------
# 模块2：布局管理（仅界面相关）
# --------------------------
class TextEditorLayout:
    def __init__(self, root, functions_instance, font_manager, text_widget):
        self.root = root
        self.functions = functions_instance
        self.font_manager = font_manager  # 接收字体管理器实例
        self.text_widget = text_widget  # 接收文本框引用

        self.create_widgets()
        self.arrange_layout()
    
    def create_widgets(self):
        # 文本框
        
        # 保存按钮
        self.save_btn = tk.Button(
            self.root, 
            text="Save", 
            command=self.functions.save_as
        )
        
        # 字体相关组件
        self.font_btn = tk.Menubutton(self.root, text="Font")
        # 通过字体管理器创建菜单
        self.font_menu = self.font_manager.create_font_menu(self.font_btn)
        # 将菜单关联到按钮
        self.font_btn["menu"] = self.font_menu
        self.font_manager.set_font("Helvetica")  # 默认字体设置为 Helvetica
    def arrange_layout(self):
        # 文本框布局
        self.text_widget.grid(row=0, column=0, sticky="nsew")
        
        # 按钮布局
        self.save_btn.grid(row=1, column=0, padx=5, pady=5)
        self.font_btn.grid(row=2, column=0, padx=5, pady=5)
        
        # 关联菜单
        self.font_btn["menu"] = self.font_menu
        
        # 配置网格权重
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

# --------------------------
# 模块3：功能实现（仅逻辑相关）
# --------------------------
class TextEditorFunctions:
    def __init__(self, text_widget):
        self.text_widget = text_widget  # 文本框引用
    
    def save_as(self):
        """保存文件功能"""
        content = self.text_widget.get("1.0", "end-1c")
        save_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        if save_path:
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(content)

# --------------------------
# 主类：协调各模块
# --------------------------
class TextEditor:
    def __init__(self, root_title="Text Editor"):
        self.root = tk.Tk(root_title)
        
        # 初始化顺序调整：
        # 1. 先创建文本框（被多个模块依赖）
        self.text_widget = tk.Text(self.root)
        
        # 2. 初始化字体管理器（需要文本框引用）
        self.font_manager = FontManager(self.text_widget)
        
        # 3. 初始化功能类（需要文本框引用）
        self.functions = TextEditorFunctions(self.text_widget)
        
        # 4. 初始化布局类（需要功能和字体管理器）
        self.layout = TextEditorLayout(
            root=self.root,
            functions_instance=self.functions,
            font_manager=self.font_manager,
            text_widget=self.text_widget
        )

    def run(self):
        self.root.mainloop()

# 运行程序
if __name__ == "__main__":
    editor = TextEditor("Simple Text Editor")
    editor.run()