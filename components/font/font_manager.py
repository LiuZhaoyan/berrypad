import tkinter as tk
from tkinter import font
from typing import Dict, List, Optional, Tuple
from core.component_manager import ComponentManager

class FontManager:
    """字体管理器 - 统一管理应用中的字体设置"""
    
    def __init__(self, manager: ComponentManager):
        self.manager = manager
        self._default_font_family = "黑体"  # 默认字体族
        self._default_font_size = 13          # 默认字体大小
        self._current_font_family = self._default_font_family
        self._current_font_size = self._default_font_size
        self._available_fonts = self._get_available_fonts()
        
        # 字体变化监听器
        self._font_change_listeners = []
        
        # 初始化字体设置
        self._initialize_font_settings()

        self._bind_events()
    
    def _get_available_fonts(self) -> List[str]:
        """获取系统可用字体列表"""
        try:
            root = tk.Tk()
            available_fonts = list(font.families())
            root.destroy()
            # 过滤常用字体并排序
            common_fonts = [
                "微软雅黑", "宋体", "黑体", "楷体", "仿宋",
                "Arial", "Times New Roman", "Courier New",
                "Helvetica", "Verdana", "Tahoma"
            ]
            # 优先显示常用字体
            result = []
            for font_name in common_fonts:
                if font_name in available_fonts:
                    result.append(font_name)
            # 添加其他可用字体
            for font_name in available_fonts:
                if font_name not in result:
                    result.append(font_name)
            return result[:50]  # 限制数量避免过多
        except Exception as e:
            print(f"获取字体列表时出错: {e}")
            return ["微软雅黑", "宋体", "黑体", "Arial", "Times New Roman"]
    
    def _initialize_font_settings(self) -> None:
        """初始化字体设置"""
        pass
    
    def _bind_events(self) -> None:
        """绑定事件"""
        self.manager.subscribe("theme.font_selected", self._on_font_selected)
        self.manager.subscribe("theme.font_size_increase", self._on_font_size_increase)
        self.manager.subscribe("theme.font_size_decrease", self._on_font_size_decrease)
        self.manager.subscribe("theme.font_size_reset", self._on_font_size_reset)
    
    def _on_font_selected(self, font_family: str) -> None:
        """处理字体选择事件"""
        self.set_font(family=font_family)
    
    def _on_font_size_increase(self) -> None:
        """处理增大字体事件"""
        self.increase_font_size(1)
    
    def _on_font_size_decrease(self) -> None:
        """处理减小字体事件"""
        self.decrease_font_size(1)
    
    def _on_font_size_reset(self) -> None:
        """处理重置字体事件"""
        self.reset_to_default()

    def set_font(self, family: str = None, size: int = None) -> bool:
        """
        设置字体
        
        Args:
            family: 字体族名称
            size: 字体大小
            
        Returns:
            bool: 设置是否成功
        """
        changed = False
        
        if family and family in self._available_fonts:
            self._current_font_family = family
            changed = True
        
        if size and 8 <= size <= 72:
            self._current_font_size = size
            changed = True
        
        if changed:
            self._notify_font_change()
            return True
        return False
    
    def reset_to_default(self) -> None:
        """重置为默认字体设置"""
        self._current_font_family = self._default_font_family
        self._current_font_size = self._default_font_size
        self._notify_font_change()
    
    def increase_font_size(self, increment: int = 1) -> None:
        """增大字体大小"""
        new_size = self._current_font_size + increment
        if new_size <= 72:
            self.set_font(size=new_size)
    
    def decrease_font_size(self, decrement: int = 1) -> None:
        """减小字体大小"""
        new_size = self._current_font_size - decrement
        if new_size >= 8:
            self.set_font(size=new_size)
    
    def _notify_font_change(self) -> None:
        """通知所有监听器字体已改变"""
        # 发布全局字体变化事件
        self.manager.publish(
            "font_changed", 
            family=self._current_font_family, 
            size=self._current_font_size
        )
        
        # 调用本地监听器
        for listener in self._font_change_listeners:
            try:
                listener(self._current_font_family, self._current_font_size)
            except Exception as e:
                print(f"调用字体变化监听器时出错: {e}")
    
    def get_current_font(self) -> Tuple[str, int]:
        """获取当前字体设置"""
        return (self._current_font_family, self._current_font_size)
    
    def get_font_object(self) -> font.Font:
        """获取当前字体对象"""
        return font.Font(family=self._current_font_family, size=self._current_font_size)
    
    def get_available_fonts(self) -> List[str]:
        """获取可用字体列表"""
        return self._available_fonts.copy()
    
    def add_font_change_listener(self, listener: callable) -> None:
        """添加字体变化监听器"""
        if listener not in self._font_change_listeners:
            self._font_change_listeners.append(listener)
    
    def remove_font_change_listener(self, listener: callable) -> None:
        """移除字体变化监听器"""
        if listener in self._font_change_listeners:
            self._font_change_listeners.remove(listener)
    
    def apply_font_to_widget(self, widget: tk.Widget, **kwargs) -> None:
        """
        应用当前字体到指定控件
        
        Args:
            widget: tkinter 控件
            **kwargs: 额外的字体属性（如 weight, slant 等）
        """
        try:
            font_config = {
                'family': self._current_font_family,
                'size': self._current_font_size
            }
            font_config.update(kwargs)
            
            widget.config(font=font.Font(**font_config))
        except Exception as e:
            print(f"应用字体到控件时出错: {e}")
    
    def get_font_metrics(self) -> Dict[str, int]:
        """获取当前字体的度量信息"""
        try:
            current_font = font.Font(family=self._current_font_family, size=self._current_font_size)
            return {
                'ascent': current_font.metrics('ascent'),
                'descent': current_font.metrics('descent'),
                'linespace': current_font.metrics('linespace'),
                'fixed': current_font.metrics('fixed')
            }
        except Exception as e:
            print(f"获取字体度量信息时出错: {e}")
            return {}
