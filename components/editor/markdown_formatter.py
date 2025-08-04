import tkinter as tk
from typing import Optional
from core.component_manager import ComponentManager

class MarkdownFormatter:
    """Markdown格式化器 - 专门处理Markdown语法逻辑"""
    
    def __init__(self, manager: ComponentManager):
        self.manager = manager
        self._bind_format_events()
    
    def _bind_format_events(self) -> None:
        """绑定所有Markdown格式化事件"""
        format_events = {
            # 基础格式
            "format.strong": self._on_strong,
            "format.emphasis": self._on_emphasis,
            "format.underline": self._on_underline,
            "format.code": self._on_code,
            "format.strike": self._on_strike,
            
            # 标题格式
            "paragraph.heading1": lambda: self._on_heading(1),
            "paragraph.heading2": lambda: self._on_heading(2),
            "paragraph.heading3": lambda: self._on_heading(3),
            "paragraph.heading4": lambda: self._on_heading(4),
            "paragraph.heading5": lambda: self._on_heading(5),
            "paragraph.heading6": lambda: self._on_heading(6),
            
            # 段落格式
            "paragraph.quote": self._on_quote,
            "paragraph.unordered_list": self._on_unordered_list,
            "paragraph.ordered_list": self._on_ordered_list,
            
            # 块格式
            "paragraph.code_block": self._on_code_block,
            "paragraph.horizontal_rule": self._on_horizontal_rule,
            
            # 链接和媒体
            "format.link": self._on_link,
            "format.image": self._on_image,
        }
        
        # 统一注册所有事件
        for event_name, handler in format_events.items():
            self.manager.subscribe(event_name, handler)
    
    def _get_active_text_area(self) -> Optional[tk.Text]:
        """获取当前活动的文本区域 - 从TextEditor继承的逻辑"""
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
    
    # ==================== 基础格式方法 ====================
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
    
    # ==================== 标题格式方法 ====================
    def _on_heading(self, level: int = 1) -> None:
        """处理多级标题 - # text"""
        if 1 <= level <= 6:
            prefix = "#" * level + " "
            self._apply_line_prefix_format(prefix)
        else:
            print(f"无效的标题级别: {level}，支持1-6级")
    
    # ==================== 段落格式方法 ====================
    def _on_quote(self) -> None:
        """处理引用格式 - > text"""
        self._apply_line_prefix_format("> ")
    
    def _on_unordered_list(self) -> None:
        """处理无序列表 - - text"""
        self._apply_line_prefix_format("- ")
    
    def _on_ordered_list(self) -> None:
        """处理有序列表 - 1. text"""
        self._apply_line_prefix_format("1. ")
    
    # ==================== 块格式方法 ====================
    def _on_code_block(self) -> None:
        """处理代码块 - ```language\n代码\n```"""
        self._apply_block_format("```\n", "\n```")
    
    def _on_horizontal_rule(self) -> None:
        """处理水平分割线 - ---"""
        self._apply_line_format("\n---\n")
    
    # ==================== 链接和媒体方法 ====================
    def _on_link(self) -> None:
        """处理链接格式 - [text](url)"""
        self._apply_placeholder_format("[", "](url)", "链接文本")
    
    def _on_image(self) -> None:
        """处理图片格式 - ![alt](url)"""
        self._apply_placeholder_format("![", "](图片URL)", "替代文本")
    
    # ==================== 核心格式化方法 ====================
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
    
    def _apply_line_prefix_format(self, prefix: str) -> None:
        """应用行前缀格式（如标题、引用、列表等）"""
        try:
            text_area = self._get_active_text_area()
            if not text_area:
                return
        
            # 检查是否有选中文本
            if text_area.tag_ranges(tk.SEL):
                # 有选中文本：为每一行添加前缀
                self._format_selected_lines(text_area, prefix)
            else:
                # 没有选中文本：为当前行添加前缀
                self._format_current_line(text_area, prefix)
                
        except Exception as e:
            print(f"应用行前缀格式时出错: {e}")
    
    def _apply_block_format(self, prefix: str, suffix: str) -> None:
        """应用块格式（如代码块等）"""
        try:
            text_area = self._get_active_text_area()
            if not text_area:
                return
        
            # 检查是否有选中文本
            if text_area.tag_ranges(tk.SEL):
                # 有选中文本：包装成块
                self._format_selected_block(text_area, prefix, suffix)
            else:
                # 没有选中文本：插入空的块格式
                self._insert_empty_block(text_area, prefix, suffix)
                
        except Exception as e:
            print(f"应用块格式时出错: {e}")
    
    def _apply_line_format(self, format_text: str) -> None:
        """应用整行格式（如分割线等）"""
        try:
            text_area = self._get_active_text_area()
            if not text_area:
                return
        
            cursor_pos = text_area.index(tk.INSERT)
            # 在当前位置插入格式文本
            text_area.insert(cursor_pos, format_text)
        
            # 将光标移动到插入文本之后
            end_pos = f"{cursor_pos}+{len(format_text)}c"
            text_area.mark_set(tk.INSERT, end_pos)
            text_area.see(end_pos)
            text_area.focus_set()
        
            # 发布光标位置事件
            self._publish_cursor_position(end_pos)
        
        except Exception as e:
            print(f"应用行格式时出错: {e}")
    
    def _apply_placeholder_format(self, prefix: str, suffix: str, placeholder: str) -> None:
        """应用占位符格式（如链接、图片等）"""
        try:
            text_area = self._get_active_text_area()
            if not text_area:
                return
        
            # 检查是否有选中文本
            if text_area.tag_ranges(tk.SEL):
                # 有选中文本：使用选中文本作为占位符内容
                self._format_selected_text_with_placeholder(text_area, prefix, suffix)
            else:
                # 没有选中文本：插入带占位符的格式
                self._insert_placeholder_format(text_area, prefix, suffix, placeholder)
                
        except Exception as e:
            print(f"应用占位符格式时出错: {e}")
    
    # ==================== 具体实现方法 ====================
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
            
            # 发布光标位置事件
            self._publish_cursor_position(new_cursor_pos)
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

        # 发布光标位置事件
        self._publish_cursor_position(middle_pos)
    
    def _format_selected_lines(self, text_area: tk.Text, prefix: str) -> None:
        """为选中的多行文本添加前缀"""
        try:
            start_pos = text_area.index(tk.SEL_FIRST)
            end_pos = text_area.index(tk.SEL_LAST)
            
            # 获取选中的起始和结束行号
            start_line = int(start_pos.split('.')[0])
            end_line = int(end_pos.split('.')[0])
            
            # 从后往前处理，避免行号变化影响
            for line_num in range(end_line, start_line - 1, -1):
                line_start = f"{line_num}.0"
                line_content = text_area.get(line_start, f"{line_num}.end")
                
                # 如果行不为空，添加前缀
                if line_content.strip():
                    text_area.insert(line_start, prefix)
            
            # 更新光标位置到最后
            final_pos = f"{end_line}.end"
            text_area.mark_set(tk.INSERT, final_pos)
            text_area.see(final_pos)
            text_area.focus_set()
            
            # 发布光标位置事件
            self._publish_cursor_position(final_pos)
            
        except Exception as e:
            print(f"格式化选中行时出错: {e}")
    
    def _format_current_line(self, text_area: tk.Text, prefix: str) -> None:
        """为当前行添加前缀"""
        try:
            cursor_pos = text_area.index(tk.INSERT)
            current_line = cursor_pos.split('.')[0]
            line_start = f"{current_line}.0"
            line_content = text_area.get(line_start, f"{current_line}.end")
            
            # 如果行不为空，添加前缀
            if line_content.strip():
                text_area.insert(line_start, prefix)
            else:
                # 如果是空行，直接插入前缀
                text_area.insert(line_start, prefix)
            
            # 将光标移动到前缀之后
            new_cursor_pos = f"{current_line}.{len(prefix)}"
            text_area.mark_set(tk.INSERT, new_cursor_pos)
            text_area.see(new_cursor_pos)
            text_area.focus_set()
            
            # 发布光标位置事件
            self._publish_cursor_position(new_cursor_pos)
            
        except Exception as e:
            print(f"格式化当前行时出错: {e}")
    
    def _format_selected_block(self, text_area: tk.Text, prefix: str, suffix: str) -> None:
        """将选中文本包装成块格式"""
        try:
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
            text_area.focus_set()
            
            # 发布光标位置事件
            self._publish_cursor_position(new_cursor_pos)
            
        except tk.TclError as e:
            # 没有选中文本的异常处理
            self._insert_empty_block(text_area, prefix, suffix)
    
    def _insert_empty_block(self, text_area: tk.Text, prefix: str, suffix: str) -> None:
        """插入空的块格式"""
        cursor_pos = text_area.index(tk.INSERT)
        
        # 插入块格式
        block_text = f"{prefix}{suffix}"
        text_area.insert(cursor_pos, block_text)
        
        # 将光标移动到前缀之后（便于输入内容）
        middle_pos = f"{cursor_pos}+{len(prefix)}c"
        text_area.mark_set(tk.INSERT, middle_pos)
        text_area.see(middle_pos)
        text_area.focus_set()
        
        # 发布光标位置事件
        self._publish_cursor_position(middle_pos)
    
    def _format_selected_text_with_placeholder(self, text_area: tk.Text, prefix: str, suffix: str) -> None:
        """使用选中文本作为占位符内容"""
        try:
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
            text_area.focus_set()
            
            # 发布光标位置事件
            self._publish_cursor_position(new_cursor_pos)
            
        except tk.TclError:
            # 没有选中文本的异常处理
            self._insert_placeholder_format(text_area, prefix, suffix, "链接文本")
    
    def _insert_placeholder_format(self, text_area: tk.Text, prefix: str, suffix: str, placeholder: str) -> None:
        """插入带占位符的格式"""
        cursor_pos = text_area.index(tk.INSERT)
        
        # 插入带占位符的格式文本
        format_text = f"{prefix}{placeholder}{suffix}"
        text_area.insert(cursor_pos, format_text)
        
        # 将光标移动到占位符文本的开始位置
        placeholder_start = f"{cursor_pos}+{len(prefix)}c"
        text_area.mark_set(tk.INSERT, placeholder_start)
        text_area.see(placeholder_start)
        text_area.focus_set()
        
        # 选中占位符文本，方便用户直接替换
        placeholder_end = f"{placeholder_start}+{len(placeholder)}c"
        text_area.tag_add(tk.SEL, placeholder_start, placeholder_end)
        
        # 发布光标位置事件
        self._publish_cursor_position(placeholder_start)
    
    @staticmethod
    def parse_cursor_position(cursor_pos: str, text_widget: tk.Text) -> tuple[int, int]:
        """
        解析 tkinter 光标位置字符串
        
        Args:
            cursor_pos: 光标位置字符串，如 "1.5" 或 "2.10+3c"
        
        """
        try:
            real_pos = text_widget.index(cursor_pos)
            line, column = real_pos.split('.')
            
            # tkinter 中行号和列号都是从1开始的
            line_num = int(line)
            col_num = int(column) + 1  # 列号转换为从1开始
            
            return line_num, col_num
        
        except ValueError as e:
            raise ValueError(f"无效的光标位置格式: {cursor_pos}") from e

    def _publish_cursor_position(self, cursor_pos: str) -> None:
        """发布光标位置事件"""
        try:
            text_area = self._get_active_text_area()
            line, column = self.parse_cursor_position(cursor_pos, text_area)
            self.manager.publish("text_cursor_moved", line=line, column=column)
        except Exception as e:
            print(f"发布光标位置时出错: {e}")