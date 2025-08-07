import logging
logger = logging.getLogger(__name__)

import tkinter as tk
from tkinter import Menu
import re
from typing import Dict, List, Tuple, Callable, Optional

class MenuManager:
    """菜单管理类"""
    def __init__(self, component_manager):
        self.manager = component_manager
        self.root = component_manager.root
        self.menu_registry: Dict[str, Dict] = {}
        self.button_map: Dict[str, tk.Button] = {}
        self.active_button: Optional[tk.Button] = None

    def register_menu(self,
                     menu_name: str,
                     button_text: str,
                     menu_items: List[Tuple[str, Callable, Optional[str]]],
                     menu_shortcut: str = "") -> None:
        """注册工具栏菜单"""
        # 创建菜单按钮
        toolbar_frame = self.manager.get_component("component_tool").toolbar_frame
        btn = tk.Button(
            toolbar_frame,
            text=button_text,
            relief=tk.FLAT,
            bd=0,
            command=lambda: self.show_menu(menu_name)
        )
        btn.pack(side=tk.LEFT, padx=2, pady=2)
        
        # 绑定悬停事件
        btn.bind("<Enter>", lambda e: self.on_button_enter(btn))
        btn.bind("<Leave>", lambda e: self.on_button_leave(btn))
        
        # 创建菜单对象
        menu = Menu(toolbar_frame, tearoff=0)
        menu_shortcut = "" if not self.is_shortcut_available(menu_shortcut, is_menu_shortcut=True) else menu_shortcut
        item_configs = []

        # 添加菜单项
        for item_name, callback, item_shortcut in menu_items:
            formatted_shortcut = self.format_shortcut(item_shortcut) if item_shortcut else ""
            menu.add_command(
                label=item_name,
                accelerator=formatted_shortcut,
                command=lambda cb=callback: self.on_menu_click(cb)
            )
            
            item_configs.append({
                "name": item_name,
                "callback": callback,
                "shortcut": item_shortcut
            })

        # 注册到菜单表
        self.menu_registry[menu_name] = {
            "button": btn,
            "menu": menu,
            "items": item_configs,
            "menu_shortcut": menu_shortcut
        }
        self.button_map[button_text] = btn

        # 绑定菜单按钮的全局快捷键
        if menu_shortcut:
            self.root.bind(menu_shortcut, lambda e: self.show_menu(menu_name))

        # 绑定所有菜单项的快捷键
        for item in item_configs:
            item_shortcut = item["shortcut"]
            if item_shortcut and item_shortcut not in ["<Control-c>", "<Control-v>", "<Control-x>"]:
                self.root.bind(item_shortcut, lambda e, cb=item["callback"]: cb())

    def show_menu(self, menu_name: str) -> None:
        """显示指定菜单"""
        if menu_name not in self.menu_registry:
            return
        config = self.menu_registry[menu_name]
        btn = config["button"]
        menu = config["menu"]
        
        x = btn.winfo_rootx() + btn.winfo_width()
        y = btn.winfo_rooty() + btn.winfo_height()
        menu.post(x, y)

    def on_button_enter(self, button: tk.Button) -> None:
        """处理按钮悬停事件"""
        self.active_button = button
        self.manager.publish("button_entered", button=button)

    def on_button_leave(self, button: tk.Button) -> None:
        """处理按钮离开事件"""
        if self.active_button == button:
            self.active_button = None
            self.manager.publish("button_leaved", button=button)

    def on_menu_click(self, callback: Callable) -> None:
        """处理菜单项点击事件"""
        if callback:
            callback()
    
    @staticmethod
    def format_shortcut(shortcut: str) -> str:
        """格式化快捷键显示"""
        # 去除首尾空格和尖括号
        shortcut = shortcut.strip()
        if shortcut.startswith('<') and shortcut.endswith('>'):
            shortcut = shortcut[1:-1]
        else:
            return shortcut
        
        # 通过"-"分割为多个部分
        parts = shortcut.split('-')
        if len(parts) < 2:
            return shortcut
        
        # 建立完整的修饰键映射
        modifier_map = {
            'Control': 'Ctrl',
            'Ctrl': 'Ctrl',
            'Alt': 'Alt',
            'Shift': 'Shift',
            'Meta': 'Meta',
            'Super': 'Super',
            'Delete': 'Delete',
            'Win': 'Win',
            'Cmd': 'Cmd',
            "bracketleft": "[",
            "bracketright": "]",
        }
        
        # 分离修饰键和主键
        if len(parts[-1]) == 1:
            # 最后一个部分是主键
            main_key = parts[-1].upper()
            modifiers = parts[:-1]
        else:
            main_key = None
            modifiers = parts
        
        # 映射修饰键
        formatted_modifiers = []
        for modifier in modifiers:
            if modifier == "Key":
                continue
            if modifier in modifier_map:
                formatted_modifiers.append(modifier_map[modifier])
            else:
                formatted_modifiers.append(modifier)
        if main_key:
            return '+'.join(formatted_modifiers) + '+' + main_key.upper()
        return '+'.join(formatted_modifiers)
    
    def is_shortcut_available(self, shortcut: str, is_menu_shortcut: bool) -> bool:
        """检查快捷键是否可用"""
        for config in self.menu_registry.values():
            if is_menu_shortcut and config["menu_shortcut"] == shortcut:
                return False
            for item in config["items"]:
                if not is_menu_shortcut and item["shortcut"] == shortcut:
                    return False
        return True

    def extend_menu(self, menu_name: str, item_name: str, callback: Callable, shortcut: str = "") -> None:
        """动态扩展菜单项"""
        if menu_name not in self.menu_registry:
            raise ValueError(f"菜单 {menu_name} 不存在")
        
        config = self.menu_registry[menu_name]
        menu = config["menu"]
        formatted_shortcut = self.format_shortcut(shortcut) if shortcut else ""
        
        menu.add_command(
            label=item_name,
            accelerator=formatted_shortcut,
            command=lambda: self.on_menu_click(callback)
        )
        
        config["items"].append({
            "name": item_name,
            "callback": callback,
            "shortcut": shortcut
        })

        if shortcut:
            self.root.bind(shortcut, lambda e: callback())