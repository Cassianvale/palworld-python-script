#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""日志封装，可设置不同等级的日志颜色"""

import logging
from logging import handlers
from typing import Text
import colorlog
import time
from pathlib import Path
import sys
import os


class LogHandler:
    """ 日志打印封装"""
    # 日志级别关系映射
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }

    def __init__(
            self,
            filename: Text,
            level: Text = "info",
            when: Text = "D",
    ):
        self.logger = logging.getLogger(filename)

        formatter = self.log_color()

        # 设置日志格式
        format_str = logging.Formatter(
            fmt="%(levelname)-8s%(asctime)s %(funcName)s py:%(lineno)d %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        # 设置日志级别
        self.logger.setLevel(self.level_relations.get(level))

        # 往屏幕上输出
        screen_output = logging.StreamHandler()
        # 设置屏幕上显示的格式
        screen_output.setFormatter(formatter)

        # 往文件里写入#指定间隔时间自动生成文件的处理器
        time_rotating = handlers.TimedRotatingFileHandler(
            filename=filename,
            when=when,
            backupCount=3,
            encoding='utf-8'
        )
        # 设置文件里写入的格式
        time_rotating.setFormatter(format_str)

        # 把对象加到logger
        # self.logger.addHandler(screen_output) # 如果不需要屏幕到终端，注释掉这行
        self.logger.addHandler(time_rotating)

    @classmethod
    def log_color(cls):
        """ 设置日志颜色 """
        log_colors_config = {
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red',
        }

        formatter = colorlog.ColoredFormatter(
            '%(log_color)s[%(asctime)s] [%(funcName)s] [%(lineno)d] [%(levelname)s]: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',  # 修改日期和时间的格式
            log_colors=log_colors_config
        )
        return formatter

    # @staticmethod
    # def add_symbol(record, symbol):
    #     """ 在日志消息前添加符号 """
    #     record.msg = f"{symbol} {record.msg}"
    #     return True


# 获取当前脚本运行的绝对路径
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    # 当脚本被 PyInstaller 打包为可执行文件时
    current_directory = os.path.dirname(sys.executable)
else:
    # 当脚本以常规方式运行时
    current_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

now_time_day = time.strftime("%Y-%m-%d", time.localtime())

logs_dir = Path(os.path.join(current_directory, "logs"))
logs_dir.mkdir(parents=True, exist_ok=True)


def add_symbol(record, level, symbol):
    """ 在特定级别的日志消息前添加符号 """
    if record.levelname == level:
        record.msg = f"{symbol} {record.msg}"
    return True


INFO = LogHandler(os.path.join(current_directory, f"logs/info-{now_time_day}.log"), level='info')
INFO.logger.addFilter(lambda record: add_symbol(record, "INFO", "✅"))
INFO.logger.addFilter(lambda record: add_symbol(record, "ERROR", "❌"))
INFO.logger.addFilter(lambda record: add_symbol(record, "WARNING", "⚠️"))

# ERROR = LogHandler(os.path.join(current_directory, f"logs/error-{now_time_day}.log"), level='error')
# ERROR.logger.addFilter(lambda record: LogHandler.add_symbol(record, "❌"))
# WARNING = LogHandler(os.path.join(current_directory, f'logs/warning-{now_time_day}.log'), level='warning')
# WARNING.logger.addFilter(lambda record: LogHandler.add_symbol(record, "⚠️"))


if __name__ == '__main__':
    print(os.path.join(current_directory, f"logs/info-{now_time_day}.log"))
    INFO.logger.info("success")
    INFO.logger.error("error")
    INFO.logger.warning("warning")
    # ERROR.logger.error("error")
    # WARNING.logger.warning("warning")
    input("Press Enter to exit...\n")
