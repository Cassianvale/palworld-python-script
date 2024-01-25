#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""日志封装，可设置不同等级的日志颜色"""

import logging
from logging import handlers
from typing import Text
import colorlog
import time
from pathlib import Path
from utils.root_path import ensure_path_sep


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

    @staticmethod
    def add_symbol(record, symbol):
        """ 在日志消息前添加符号 """
        record.msg = f"{symbol} {record.msg}"
        return True


now_time_day = time.strftime("%Y-%m-%d", time.localtime())

logs_dir = Path(ensure_path_sep("/logs"))
logs_dir.mkdir(parents=True, exist_ok=True)

INFO = LogHandler(ensure_path_sep(f"\\logs\\info-{now_time_day}.log"), level='info')
INFO.logger.addFilter(lambda record: LogHandler.add_symbol(record, "✅"))
ERROR = LogHandler(ensure_path_sep(f"\\logs\\error-{now_time_day}.log"), level='error')
ERROR.logger.addFilter(lambda record: LogHandler.add_symbol(record, "❌"))
WARNING = LogHandler(ensure_path_sep(f'\\logs\\warning-{now_time_day}.log'), level='warning')
WARNING.logger.addFilter(lambda record: LogHandler.add_symbol(record, "⚠️"))

if __name__ == '__main__':
    INFO.logger.info("success")
    ERROR.logger.error("error")
    WARNING.logger.warning("warning")
