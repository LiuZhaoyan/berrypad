import logging
logger = logging.getLogger(__name__)

from typing import Callable
# --------------------------
# 组件管理系统与事件总线
# --------------------------

class EventBus:
    """事件总线实现"""
    def __init__(self):
        self.subscribers = {}
    
    def subscribe(self, event_name: str, callback: Callable) -> None:
        if event_name not in self.subscribers:
            self.subscribers[event_name] = []
        self.subscribers[event_name].append(callback)
        logger.info(f"订阅事件: {event_name} -> {callback.__name__}")
    
    def unsubscribe(self, event_type: str, callback: Callable) -> None:
        """取消订阅事件"""
        if event_type in self._subscribers:
            self._subscribers[event_type].remove(callback)

    def publish(self, event_name: str, **payload) -> None:
        logger.info(f"发布事件: {event_name}")
        if event_name in self.subscribers.keys():
            for callback in self.subscribers[event_name]:
                try:
                    callback(**payload)
                except Exception as e:
                    logger.error(f"事件回调执行错误: {event_name} - {str(e)}")
