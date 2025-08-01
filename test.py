import tkinter as tk
from tkinter import ttk

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("文本编辑器")
        self.root.geometry("600x400")
        
        # 创建文本框
        self.text_widget = tk.Text(root, wrap=tk.WORD)
        self.text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建滚动条
        scrollbar = ttk.Scrollbar(self.text_widget)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_widget.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.text_widget.yview)
        
        # 创建菜单栏
        self.create_menu()
        
        # 绑定快捷键
        # self.bind_shortcuts()
    
    def create_menu(self):
        # 创建菜单栏
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 编辑菜单
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="编辑", menu=edit_menu)
        edit_menu.add_command(label="复制", command=self.copy_text, accelerator="Ctrl+C")
        edit_menu.add_command(label="剪切", command=self.cut_text, accelerator="Ctrl+X")
        edit_menu.add_command(label="粘贴", command=self.paste_text, accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="全选", command=self.select_all, accelerator="Ctrl+A")
    
    def bind_shortcuts(self):
        # 绑定快捷键
        self.root.bind('<Control-c>', lambda e: self.copy_text())
        self.root.bind('<Control-x>', lambda e: self.cut_text())
        self.root.bind('<Control-v>', lambda e: self.paste_text())
        self.root.bind('<Control-a>', lambda e: self.select_all())
    
    def copy_text(self):
        try:
            # 复制选中的文本到剪贴板
            selected_text = self.text_widget.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.root.clipboard_clear()
            self.root.clipboard_append(selected_text)
        except tk.TclError:
            # 没有选中文本时的处理
            pass
    
    def cut_text(self):
        try:
            # 剪切选中的文本
            selected_text = self.text_widget.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.root.clipboard_clear()
            self.root.clipboard_append(selected_text)
            self.text_widget.delete(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            pass
    
    def paste_text(self):
        try:
            # 从剪贴板粘贴文本
            clipboard_text = self.root.clipboard_get()
            # 在光标位置插入文本
            self.text_widget.insert(tk.INSERT, clipboard_text)
        except tk.TclError:
            pass
    
    def select_all(self):
        # 全选文本
        self.text_widget.tag_add(tk.SEL, "1.0", tk.END)
        self.text_widget.mark_set(tk.INSERT, "1.0")
        self.text_widget.see(tk.INSERT)

if __name__ == "__main__":
    root = tk.Tk()
    app = TextEditor(root)
    root.mainloop()
