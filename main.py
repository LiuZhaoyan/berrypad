# 配置日志系统
import logging
import sys
from logging import StreamHandler

def configure_logging(level: int = logging.INFO) -> None:
    """
    全局配置日志输出到终端（不生成文件）
    
    Args:
        level: 日志级别（默认INFO，可选DEBUG/INFO/WARNING/ERROR/CRITICAL）
    """
    # 避免重复配置（如果已经配置过则跳过）
    if logging.root.handlers:
        return

    # 定义日志格式（可根据需求调整）
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # 配置终端输出（使用StreamHandler指向标准输出）
    console_handler = StreamHandler(sys.stdout)
    console_handler.setLevel(level)  # 处理器级别（过滤低于此级别的日志）
    
    # 设置日志格式
    formatter = logging.Formatter(log_format)
    console_handler.setFormatter(formatter)
    
    # 配置根日志器
    root_logger = logging.getLogger()
    root_logger.setLevel(level)  # 根日志器级别（全局最低级别）
    root_logger.addHandler(console_handler)
logger = logging.getLogger(__name__)

from app import MarkdownEditorApp

if __name__ == "__main__":
    configure_logging(logging.DEBUG)  # 设置日志级别为DEBUG
    app = MarkdownEditorApp()
    app.run()