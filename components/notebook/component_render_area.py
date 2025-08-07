import tkinter as tk
import re
from core.component_basic import ComponentBasic
from core.component_manager import ComponentManager


class MarkdownRenderer:
    """Markdown渲染器 - 高效增量渲染"""

    def __init__(self, render_text: tk.Text):
        self.render_text = render_text
        self._blocks = []  # 缓存已渲染的块
        self._current_content = ""
        self._setup_tags()

    def _setup_tags(self):
        """设置文本样式标签"""
        # 标题样式
        self.render_text.tag_configure("h1", font=("Microsoft YaHei", 18, "bold"),
                                       spacing1=16, spacing3=8)
        self.render_text.tag_configure("h2", font=("Microsoft YaHei", 16, "bold"),
                                       spacing1=14, spacing3=7)
        self.render_text.tag_configure("h3", font=("Microsoft YaHei", 14, "bold"),
                                       spacing1=12, spacing3=6)
        self.render_text.tag_configure("h4", font=("Microsoft YaHei", 13, "bold"),
                                       spacing1=10, spacing3=5)
        self.render_text.tag_configure("h5", font=("Microsoft YaHei", 12, "bold"),
                                       spacing1=8, spacing3=4)
        self.render_text.tag_configure("h6", font=("Microsoft YaHei", 11, "bold"),
                                       spacing1=6, spacing3=3)

        # 代码样式
        self.render_text.tag_configure("code", font=("Consolas", 11),
                                       background="#f6f8fa", foreground="#24292e")
        self.render_text.tag_configure("code_block", font=("Consolas", 11),
                                       background="#f6f8fa", lmargin1=20, lmargin2=20,
                                       spacing1=8, spacing3=8)

        # 引用样式
        self.render_text.tag_configure("quote", background="#f0f0f0",
                                       lmargin1=15, lmargin2=15,
                                       foreground="#6a737d", spacing1=4, spacing3=4)

        # 列表样式
        self.render_text.tag_configure("list_item", lmargin1=20, lmargin2=20,
                                       spacing1=2, spacing3=2)

        # 分割线样式
        self.render_text.tag_configure("hr", background="#e1e4e8",
                                       spacing1=1, spacing3=1)

        # 行内样式
        self.render_text.tag_configure("bold", font=("Microsoft YaHei", 12, "bold"))
        self.render_text.tag_configure("italic", font=("Microsoft YaHei", 12, "italic"))
        self.render_text.tag_configure("bold italic", font=("Microsoft YaHei", 12, "bold italic"))
        self.render_text.tag_configure("strikethrough", overstrike=True)
        self.render_text.tag_configure("link", foreground="#0366d6", underline=True)

    @staticmethod
    def _is_horizontal_rule(line: str) -> bool:
        """检查是否为分割线"""
        hr_patterns = [
            r'^\s*-{3,}\s*$',  # ---
            r'^\s*\*{3,}\s*$',  # ***
            r'^\s*_{3,}\s*$',  # ___
            r'^\s*\+{3,}\s*$',  # +++
        ]
        return any(re.match(p, line) for p in hr_patterns)

    @staticmethod
    def _parse_header(line: str):
        """解析标题"""
        match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if match:
            return len(match.group(1)), match.group(2)
        return None

    @staticmethod
    def _is_list_item(line: str) -> bool:
        """检查是否为列表项"""
        return bool(re.match(r'^\s*[-*+]\s+', line) or re.match(r'^\s*\d+\.\s+', line))

    @staticmethod
    def _parse_list_item(line: str):
        """解析列表项"""
        match = re.match(r'^\s*([-*+]|\d+\.)\s+(.+)$', line)
        if match:
            return match.group(1), match.group(2)
        return None, line

    @staticmethod
    def _format_inline_elements(text: str):
        """格式化行内元素，返回 [(text, [tags])]"""
        patterns = [
            (re.compile(r'`(.*?)`'), 'code'),
            (re.compile(r'~~(.*?)~~'), 'strikethrough'),
            (re.compile(r'\*\*\*(.*?)\*\*\*|___(.*?)___'), 'bold italic'),
            (re.compile(r'\*\*(.*?)\*\*|__(.*?)__'), 'bold'),
            (re.compile(r'\*(.*?)\*|_(.*?)_'), 'italic'),
        ]

        result = []
        pos = 0

        while pos < len(text):
            # 查找最近的特殊字符
            next_special = len(text)
            for pattern, tag in patterns:
                m = pattern.search(text, pos)
                if m and m.start() < next_special:
                    next_special = m.start()

            # 添加普通文本
            if pos < next_special:
                result.append((text[pos:next_special], []))
                pos = next_special

            # 处理特殊格式
            if pos < len(text):
                found = False
                for pattern, tag in patterns:
                    m = pattern.match(text, pos)
                    if m:
                        content = next(g for g in m.groups() if g is not None)
                        result.append((content, [tag]))
                        pos = m.end()
                        found = True
                        break
                if not found:
                    result.append((text[pos], []))
                    pos += 1

        return result

    @staticmethod
    def _process_hard_line_breaks(text: str) -> str:
        """处理硬换行（行尾两个空格）"""
        return re.sub(r'  $', '\n', text)

    def _classify_block(self, lines: list) -> dict:
        """将一组行分类为一个块"""
        if not lines:
            return {"type": "empty"}

        line = lines[0].strip()
        if not line:
            return {"type": "empty"}
        elif self._is_horizontal_rule(line):
            return {"type": "hr"}
        elif self._parse_header(line):
            level, text = self._parse_header(line)
            return {"type": "header", "level": level, "text": text}
        elif line.startswith('```'):
            code_lines = []
            for l in lines[1:]:
                if l.strip().startswith('```'):
                    break
                code_lines.append(l)
            return {"type": "code", "lines": code_lines}
        elif line.startswith('>'):
            quote_lines = [l[1:].lstrip() if l.strip().startswith('>') else l for l in lines]
            quote_lines = [l[1:].lstrip() if l.strip().startswith('>') else l for l in quote_lines]
            # 清理引用标记
            cleaned_lines = []
            for l in quote_lines:
                if l.strip().startswith('>'):
                    cleaned_lines.append(l[1:].lstrip())
                else:
                    cleaned_lines.append(l)
            return {"type": "quote", "lines": cleaned_lines}
        elif self._is_list_item(line):
            items = []
            for l in lines:
                if self._is_list_item(l):
                    marker, text = self._parse_list_item(l)
                    items.append((marker, text))
            return {"type": "list", "items": items}
        else:
            return {"type": "para", "lines": lines}

    def _render_block(self, block: dict):
        """渲染一个块"""
        t = self.render_text
        start_index = t.index("end-1c")

        if block["type"] == "hr":
            t.insert("end", " " * 20 + "\n", "hr")
        elif block["type"] == "header":
            t.insert("end", block["text"] + "\n", f"h{block['level']}")
        elif block["type"] == "code":
            for line in block["lines"]:
                t.insert("end", (line or "") + "\n", "code_block")
        elif block["type"] == "quote":
            quote_text = "\n".join(block["lines"])
            t.insert("end", quote_text + "\n", "quote")
        elif block["type"] == "list":
            for marker, text in block["items"]:
                # 统一使用圆点作为列表标记
                t.insert("end", f"• {text}\n", "list_item")
        elif block["type"] == "para":
            para_text = ' '.join(line.rstrip() for line in block["lines"])
            para_text = self._process_hard_line_breaks(para_text)
            fragments = self._format_inline_elements(para_text)
            for frag, tags in fragments:
                t.insert("end", frag, tuple(tags) if tags else None)
            t.insert("end", "\n")
        elif block["type"] == "empty":
            t.insert("end", "\n")

        end_index = t.index("end-1c")
        return start_index, end_index

    def update_content(self, new_content: str):
        """
        增量更新内容（用于实时渲染）
        """
        # 为简化实现，此处使用全量重绘
        # 实际项目中可以优化为只更新差异块
        self.render_text.config(state="normal")
        self.render_text.delete("1.0", "end")

        if not new_content:
            self.render_text.config(state="disabled")
            return

        # 分块处理
        lines = new_content.split('\n')
        self._blocks = []

        i = 0
        block_start = 0

        # 重新分块
        while i < len(lines):
            line = lines[i].strip()

            # 空行处理
            if not line:
                if i > block_start:
                    block_lines = lines[block_start:i]
                    if block_lines:
                        self._blocks.append(self._classify_block(block_lines))
                self._blocks.append({"type": "empty"})
                i += 1
                block_start = i
                continue

            # 分割线处理
            if self._is_horizontal_rule(lines[i]):
                if i > block_start:
                    block_lines = lines[block_start:i]
                    if block_lines:
                        self._blocks.append(self._classify_block(block_lines))
                self._blocks.append({"type": "hr"})
                i += 1
                block_start = i
                continue

            # 代码块处理
            if lines[i].strip().startswith('```'):
                j = i + 1
                while j < len(lines) and not lines[j].strip().startswith('```'):
                    j += 1
                if j < len(lines):
                    j += 1
                code_block = {"type": "code", "lines": lines[i + 1:j - 1]}
                if i > block_start:
                    block_lines = lines[block_start:i]
                    if block_lines:
                        self._blocks.append(self._classify_block(block_lines))
                self._blocks.append(code_block)
                i = j
                block_start = i
                continue

            # 引用块处理
            if lines[i].strip().startswith('>'):
                j = i
                while j < len(lines) and lines[j].strip().startswith('>'):
                    j += 1
                quote_lines = [l[1:].lstrip() if l.strip().startswith('>') else l for l in lines[i:j]]
                quote_block = {"type": "quote", "lines": quote_lines}
                if i > block_start:
                    block_lines = lines[block_start:i]
                    if block_lines:
                        self._blocks.append(self._classify_block(block_lines))
                self._blocks.append(quote_block)
                i = j
                block_start = i
                continue

            # 列表处理
            if self._is_list_item(lines[i]):
                j = i
                while j < len(lines) and self._is_list_item(lines[j]):
                    j += 1
                list_items = []
                for k in range(i, j):
                    marker, text = self._parse_list_item(lines[k])
                    list_items.append((marker, text))
                list_block = {"type": "list", "items": list_items}
                if i > block_start:
                    block_lines = lines[block_start:i]
                    if block_lines:
                        self._blocks.append(self._classify_block(block_lines))
                self._blocks.append(list_block)
                i = j
                block_start = i
                continue

            # 标题处理
            header = self._parse_header(lines[i])
            if header:
                header_block = {"type": "header", "level": header[0], "text": header[1]}
                if i > block_start:
                    block_lines = lines[block_start:i]
                    if block_lines:
                        self._blocks.append(self._classify_block(block_lines))
                self._blocks.append(header_block)
                i += 1
                block_start = i
                continue

            i += 1

        # 处理最后的块
        if block_start < len(lines):
            block_lines = lines[block_start:]
            if any(line.strip() for line in block_lines):
                self._blocks.append(self._classify_block(block_lines))

        # 渲染所有块
        for block in self._blocks:
            if block["type"] != "empty":
                self._render_block(block)

        self.render_text.config(state="disabled")


class ComponentRenderArea(ComponentBasic):
    """Markdown 渲染区域组件 - 高效实时渲染版"""

    def __init__(self, manager: ComponentManager):
        super().__init__(
            name="render_area",
            manager=manager
        )
        self.render_text = None
        self.markdown_renderer = None
        self.in_sync = False
        self.last_scroll_position = 0.0
        self.current_content = ""
        self._render_debounce_id = None  # 防抖定时器ID
        self._render_debounce_delay = 50  # 防抖延迟（毫秒）

        self._init_render_area()

    def _init_render_area(self):
        """初始化渲染区域"""
        # 订阅事件
        self.manager.subscribe("text_scrolled", self.on_text_scrolled)
        self.manager.subscribe("text_updated", self._on_text_updated_debounced)
        self.manager.subscribe("tab_switched", self._on_tab_switched_render)

    def create_render_area(self):
        """创建美化文本渲染区域"""
        container = self.get_container()

        # 创建主框架
        main_frame = tk.Frame(container)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 创建文本区域
        self.render_text = tk.Text(
            main_frame,
            wrap=tk.WORD,
            background="#ffffff",
            foreground="#24292e",
            font=("Microsoft YaHei", 12),
            padx=25,
            pady=25,
            spacing1=6,
            spacing2=2,
            spacing3=6,
            relief=tk.FLAT,
            borderwidth=0
        )

        self.render_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 初始化Markdown渲染器
        self.markdown_renderer = MarkdownRenderer(self.render_text)

        # 显示初始内容
        self._display_welcome_message()

    def _display_welcome_message(self):
        """显示欢迎消息"""
        self.render_text.config(state=tk.NORMAL)
        self.render_text.delete(1.0, tk.END)
        self.render_text.insert(tk.END, "Markdown 预览区域\n", "h2")
        self.render_text.insert(tk.END, "在这里查看您的 Markdown 文档渲染效果\n\n")
        self.render_text.insert(tk.END, "开始编辑左侧的文档，预览将实时显示在这里。")
        self.render_text.config(state=tk.DISABLED)

    def _on_text_updated_debounced(self, content: str):
        """防抖处理文本更新事件"""
        # 取消之前的定时器
        if self._render_debounce_id:
            self.manager.root.after_cancel(self._render_debounce_id)

        # 设置新的定时器
        self._render_debounce_id = self.manager.root.after(
            self._render_debounce_delay,
            lambda: self._on_text_updated(content)
        )

    def _on_text_updated(self, content: str):
        """处理文本更新事件"""
        # 清除防抖定时器ID
        self._render_debounce_id = None

        # 保存滚动位置
        self._save_scroll_position()

        # 渲染内容
        self._render_markdown_content(content)

        # 恢复滚动位置
        self._restore_scroll_position()

        # 更新内容记录
        self.current_content = content

    def _save_scroll_position(self):
        """保存滚动位置"""
        try:
            current_view = self.render_text.yview()
            if current_view and len(current_view) >= 2:
                self.last_scroll_position = current_view[0]
        except:
            self.last_scroll_position = 0.0

    def _restore_scroll_position(self):
        """恢复滚动位置"""
        if not self.current_content:  # 首次加载不恢复位置
            return
        try:
            self.render_text.yview_moveto(self.last_scroll_position)
        except:
            pass

    def _render_markdown_content(self, content: str):
        """使用Markdown渲染器渲染内容"""
        if not content:
            self._display_empty_content()
            return

        try:
            # 使用高效的Markdown渲染器
            self.markdown_renderer.update_content(content)
        except Exception as e:
            self._display_error_content(str(e))

    def _display_empty_content(self):
        """显示空内容"""
        self.render_text.config(state=tk.NORMAL)
        self.render_text.delete(1.0, tk.END)
        self.render_text.insert(tk.END, "暂无内容\n\n", "h2")
        self.render_text.insert(tk.END, "开始编辑文档以查看预览效果。")
        self.render_text.config(state=tk.DISABLED)

    def _display_error_content(self, error_message: str):
        """显示错误内容"""
        self.render_text.config(state=tk.NORMAL)
        self.render_text.delete(1.0, tk.END)
        self.render_text.insert(tk.END, "渲染错误\n", "h2")
        self.render_text.insert(tk.END, f"错误信息: {error_message}\n\n")
        self.render_text.insert(tk.END, "请检查您的 Markdown 语法是否正确。")
        self.render_text.config(state=tk.DISABLED)

    def on_text_scrolled(self, fraction):
        """处理滚动同步"""
        if self.in_sync or not self.render_text:
            return

        if not self.current_content:  # 首次加载不同步
            return

        self.in_sync = True
        try:
            self.render_text.yview_moveto(fraction)
        except:
            pass
        finally:
            self.in_sync = False

    def _on_tab_switched_render(self, new_tab_frame: tk.Frame):
        """处理标签页切换"""
        try:
            notebook_component = self.manager.get_component("component_notebook")
            if not notebook_component:
                return

            current_tab_name = notebook_component.get_current_tab_name()
            if current_tab_name and current_tab_name in notebook_component.tab_content_cache:
                cached_content = notebook_component.tab_content_cache[current_tab_name]
                # 立即渲染，不需要防抖
                self._on_text_updated(cached_content)
            else:
                self._display_welcome_message()
                self.last_scroll_position = 0.0
                self.current_content = ""

        except Exception as e:
            print(f"标签页切换错误: {e}")

    def get_layout_section(self):
        return "render_section"

    def set_render_debounce_delay(self, delay_ms: int):
        """设置渲染防抖延迟（毫秒）"""
        self._render_debounce_delay = max(10, delay_ms)  # 最小10ms