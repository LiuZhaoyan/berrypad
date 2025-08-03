import tkinter as tk
from tkinter import filedialog, messagebox
import os

from core.component_basic import ComponentBasic
from core.component_manager import ComponentManager

class TextEditor(ComponentBasic):
    """文本编辑器组件"""
    def __init__(self, manager: ComponentManager):
        super().__init__(name="text_editor", manager=manager)
        self.tab_file_paths = {}  # 每个标签页对应的文件路径 {tab_name: file_path}
        self._bind_events()
        self._setup_tab_events()
    
    def _bind_events(self) -> None:
        """订阅全局事件"""
        self.manager.subscribe("file.new", self._on_new_file)
        self.manager.subscribe("file.open", self._on_open_file)
        self.manager.subscribe("file.save", self._on_save_file)
        self.manager.subscribe("file.save_as", self._on_save_as_file)
        self.manager.subscribe("edit.copy", self._on_copy)
        self.manager.subscribe("edit.paste", self._on_paste)
        self.manager.subscribe("edit.cut", self._on_cut)
        self.manager.subscribe("format.strong", self._on_strong)
        self.manager.subscribe("format.emphasis", self._on_emphasis)
        self.manager.subscribe("format.underline", self._on_underline)
        self.manager.subscribe("format.code", self._on_code)
        self.manager.subscribe("format.strike", self._on_strike)
    
    def _setup_tab_events(self) -> None:
        """订阅标签页相关事件"""
        self.manager.subscribe("tab_switched", self._on_tab_switched)
        self.manager.subscribe("new_tab_generated", self._on_new_tab_generated)
    
    def _on_new_tab_generated(self, tab_name: str) -> None:
        """处理新标签页创建事件"""
        self.tab_file_paths[tab_name] = None  # 新标签页没有关联文件
    
    def _on_tab_switched(self, new_tab_frame) -> None:
        """处理标签页切换事件"""
        notebook = self.manager.get_component("component_notebook")
        if not notebook:
            return
            
        current_tab_name = notebook.get_current_tab_name()
        if current_tab_name:
            # 获取该标签页对应的文件路径
            file_path = self.tab_file_paths.get(current_tab_name)
            
            # 更新状态栏
            status_component = self.manager.get_component("component_status")
            if status_component:
                if file_path:
                    status_component.set_status(f"文件: {file_path}")
                    # 可以添加文件修改状态检测
                else:
                    status_component.set_status(f"未命名文档: {current_tab_name}")
                
                # 更新编码信息
                status_component.set_encoding("UTF-8")
    
    def _on_new_file(self) -> None:
        """新建文件 - 创建新标签页"""
        notebook = self.manager.get_component("component_notebook")
        if notebook:
            # 生成唯一标签名
            tab_count = len(notebook._tabs) + 1
            tab_name = f"Untitled {tab_count}" # TODO: 可优化
            new_tab = notebook.add_tab(tab_name)
            
            # 初始化该标签页的文件路径
            self.tab_file_paths[tab_name] = None
            
            # 更新状态栏
            status_component = self.manager.get_component("component_status")
            if status_component:
                status_component.set_status(f"已创建新文件: {tab_name}")
                status_component.set_encoding("UTF-8")
    
    def _on_open_file(self) -> None:
        """打开文件"""
        try:
            # 打开文件选择对话框
            file_path = filedialog.askopenfilename(
                title="打开文件",
                filetypes=[
                    ("Markdown文件", "*.md"),
                    ("文本文件", "*.txt"),
                    ("所有文件", "*.*")
                ]
            )
            
            if file_path:  # 用户选择了文件
                # 读取文件内容
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                # 获取或创建Notebook组件
                notebook = self.manager.get_component("component_notebook")
                if not notebook:
                    return
                
                # 生成标签名（使用文件名）
                file_name = os.path.basename(file_path)
                tab_name = file_name
                
                # 检查是否已存在同名标签页
                existing_tab = notebook.get_tab_by_name(tab_name)
                if existing_tab:
                    # 如果存在，切换到该标签页并更新内容
                    notebook.switch_tab_by_name(tab_name)
                    text_area = self._get_active_text_area()
                    if text_area:
                        text_area.delete(1.0, tk.END)
                        text_area.insert(1.0, content)
                    
                    # 更新该标签页的文件路径
                    self.tab_file_paths[tab_name] = file_path
                else:
                    # 创建新标签页
                    new_tab = notebook.add_tab(tab_name)
                    # 等待文本区域创建完成后再设置内容
                    self.manager.root.after(100, lambda: self.set_file_path(tab_name, content, file_path))
                
                # 更新状态栏
                status_component = self.manager.get_component("component_status")
                if status_component:
                    status_component.set_status(f"已打开文件: {file_path}")
                    status_component.set_encoding("UTF-8")
                    # 更新光标位置（简单示例）
                    status_component.set_cursor_position(1, 1)
                
        except UnicodeDecodeError:
            messagebox.showerror("错误", "文件编码不支持，请选择UTF-8编码的文件")
        except Exception as e:
            messagebox.showerror("错误", f"打开文件失败: {str(e)}")

    def _on_save_file(self) -> None:
        """保存文件"""
        try:
            # 获取当前标签页名称
            notebook = self.manager.get_component("component_notebook")
            if not notebook:
                return
                
            current_tab_name = notebook.get_current_tab_name()
            if not current_tab_name:
                return
            
            # 获取当前文本内容
            text_area = self._get_active_text_area()
            if not text_area:
                return
                
            content = text_area.get(1.0, tk.END).strip()
            
            # 检查该标签页是否有已保存的文件路径
            current_file_path = self.tab_file_paths.get(current_tab_name)
            if current_file_path:
                # 直接保存到原文件
                with open(current_file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                
                # 更新状态栏
                status_component = self.manager.get_component("component_status")
                if status_component:
                    status_component.set_status(f"文件已保存: {current_file_path}")
            else:
                # 没有文件路径，执行另存为
                self._on_save_as_file()
                
        except Exception as e:
            messagebox.showerror("错误", f"保存文件失败: {str(e)}")
    
    def _on_save_as_file(self) -> None:
        """另存为文件"""
        try:
            # 获取当前标签页名称和内容
            notebook = self.manager.get_component("component_notebook")
            if not notebook:
                return
                
            current_tab_name = notebook.get_current_tab_name()
            if not current_tab_name:
                return
            
            text_area = self._get_active_text_area()
            if not text_area:
                return
                
            content = text_area.get(1.0, tk.END).strip()
            
            # 打开保存对话框
            default_extension = ".md"
            file_path = filedialog.asksaveasfilename(
                title="保存文件",
                defaultextension=default_extension,
                filetypes=[
                    ("Markdown文件", "*.md"),
                    ("文本文件", "*.txt"),
                    ("所有文件", "*.*")
                ]
            )
            
            if file_path:  # 用户选择了保存路径
                # 保存文件
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                
                # 更新该标签页的文件路径
                self.tab_file_paths[current_tab_name] = file_path
                
                # 更新标签页名称（如果需要）
                file_name = os.path.basename(file_path)
                if file_name != current_tab_name:
                    # 更新标签页标题
                    notebook.set_tab_name(current_tab_name, file_name)
                    self.tab_file_paths[file_name] = self.tab_file_paths.pop(current_tab_name, None)
                
                # 更新状态栏
                status_component = self.manager.get_component("component_status")
                if status_component:
                    status_component.set_status(f"文件已保存: {file_path}")
                    status_component.set_encoding("UTF-8")
                    
        except Exception as e:
            messagebox.showerror("错误", f"保存文件失败: {str(e)}")
    
    def _on_copy(self) -> None:
        """复制"""
        try:
            text_area = self._get_active_text_area()
            if text_area:
                text_area.clipboard_clear()
                text = text_area.get(tk.SEL_FIRST, tk.SEL_LAST)
                text_area.clipboard_append(text)
        except tk.TclError:
            pass  # 没有选中文本
    
    def _on_paste(self) -> None:
        """粘贴"""
        try:
            text_area = self._get_active_text_area()
            if text_area:
                text = text_area.clipboard_get()
                text_area.insert(tk.INSERT, text)
        except tk.TclError:
            pass
    
    def _on_cut(self) -> None:
        """剪切"""
        self._on_copy()
        try:
            text_area = self._get_active_text_area()
            if text_area:
                text_area.delete(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            pass  # 没有选中文本
    
    def set_file_path(self, tab_name: str, content: str, file_path: str) -> None:
        """设置文件路径"""
        notebook = self.manager.get_component("component_notebook")
        if not notebook:
            return
        # 文件内容写入当前标签页的文本区域
        text_area = self._get_active_text_area()
        if text_area:
            text_area.delete(1.0, tk.END)
            text_area.insert(1.0, content)
        
        # 更新文件路径映射
        self.tab_file_paths[tab_name] = file_path
    
    def get_file_path_for_tab(self, tab_name: str) -> str:
        """获取指定标签页的文件路径"""
        return self.tab_file_paths.get(tab_name)
    
    def set_file_path_for_tab(self, tab_name: str, file_path: str) -> None:
        """设置指定标签页的文件路径"""
        self.tab_file_paths[tab_name] = file_path
    
    def get_current_tab_file_path(self) -> str:
        """获取当前标签页的文件路径"""
        notebook = self.manager.get_component("component_notebook")
        if notebook:
            current_tab_name = notebook.get_current_tab_name()
            if current_tab_name:
                return self.tab_file_paths.get(current_tab_name)
        return None
    
    # =================== 格式化操作 ===================    
    
    def _on_strong(self) -> None:
        """处理粗体格式 - **text**"""
        self._apply_markdown_format("**", "**")
    
    def _on_emphasis(self) -> None:
        """处理斜体格式 - *text*"""
        self._apply_markdown_format("*", "*")

    def _on_underline(self) -> None:
        """处理下划线格式 - <u>text</u>"""
        self._apply_markdown_format("<u>", "</u>")
    
    def _on_code(self) -> None:
        """处理单行代码格式 - `code`"""
        self._apply_markdown_format("`", "`")

    def _on_strike(self) -> None:
        """处理删除线格式 - ~~text~~"""
        self._apply_markdown_format("~~", "~~")
    
    def _apply_markdown_format(self, prefix: str, suffix: str) -> None:
        """应用Markdown格式的通用方法"""
        try:
            text_area = self._get_active_text_area()
            if not text_area:
                return
            
            # 检查是否有选中文本
            if text_area.tag_ranges(tk.SEL):
                # 有选中文本：在选中文本周围添加格式符号
                self._format_selected_text(text_area, prefix, suffix)
            else:
                # 没有选中文本：插入空的格式符号并将光标放在中间
                self._insert_empty_format(text_area, prefix, suffix)
                
        except Exception as e:
            print(f"应用Markdown格式时出错: {e}")
    
    def _format_selected_text(self, text_area: tk.Text, prefix: str, suffix: str) -> None:
        """格式化选中的文本"""
        try:
            # 获取选中文本的起始和结束位置
            start_pos = text_area.index(tk.SEL_FIRST)
            end_pos = text_area.index(tk.SEL_LAST)
            
            # 获取选中的文本内容
            selected_text = text_area.get(start_pos, end_pos)
            
            # 删除选中的文本
            text_area.delete(start_pos, end_pos)
            
            # 在原位置插入带格式的文本
            formatted_text = f"{prefix}{selected_text}{suffix}"
            text_area.insert(start_pos, formatted_text)
            
            # 设置新的光标位置（在格式化文本之后）
            new_cursor_pos = f"{start_pos}+{len(formatted_text)}c"
            text_area.mark_set(tk.INSERT, new_cursor_pos)
            text_area.see(new_cursor_pos)
            
            # 解析行号和列号（注意：Tkinter行号从1开始，列号从0开始）
            line, column = new_cursor_pos.split('.')
            line = int(line)
            col = int(column) + 1
            
            # 发布光标位置事件
            self.manager.publish("text_cursor_moved", line=line, column=col)
        except tk.TclError:
            # 没有选中文本的异常处理
            self._insert_empty_format(text_area, prefix, suffix)
    
    def _insert_empty_format(self, text_area: tk.Text, prefix: str, suffix: str) -> None:
        """插入空的格式符号"""
        cursor_pos = text_area.index(tk.INSERT)
        
        # 插入格式符号
        format_text = f"{prefix}{suffix}"
        text_area.insert(cursor_pos, format_text)
        
        # 将光标移动到符号中间
        middle_pos = f"{cursor_pos}+{len(prefix)}c"
        text_area.mark_set(tk.INSERT, middle_pos)
        text_area.see(middle_pos)
        
        # 确保光标可见
        text_area.focus_set()

        # 解析行号和列号（注意：Tkinter行号从1开始，列号从0开始）
        line, column = middle_pos.split('.')
        line = int(line)
        col = int(column) + 1
        
        # 发布光标位置事件
        self.manager.publish("text_cursor_moved", line=line, column=col)
    
    def _get_active_text_area(self) -> tk.Text:
        """获取当前活动的文本区域"""
        # 首先尝试从文本区域组件获取
        text_area_component = self.manager.get_component("text_area")
        if text_area_component:
            # 优先返回当前活动的文本区域
            if text_area_component.text_area:
                return text_area_component.text_area
        
        # 备选方案：尝试从焦点获取
        focused_widget = self.manager.root.focus_get()
        if isinstance(focused_widget, tk.Text):
            return focused_widget
        
        return None