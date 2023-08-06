#!/usr/bin/env python3
# coding = utf8
"""
@ Author : ZeroSeeker
@ e-mail : zeroseeker@foxmail.com
@ GitHub : https://github.com/ZeroSeeker
@ Gitee : https://gitee.com/ZeroSeeker

feature: 提供日志记录功能的模块，与python自带的logging兼容
但是不要调用logging里的basicConfig方法，否则会影响此模块的使用
将log存储文件的编码改为了utf-8
"""
from functools import wraps
from colorama import init
import logging
import sys
import os
init(autoreset=True)


def singleton(cls):
    instances = {}

    @wraps(cls)
    def get_instance(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return get_instance


@singleton
class LoggerWrapper(object):
    """
    best practice是不适用logging模块，仅使用本模块，导入easylog后，像使用logging.info等一样使用easylog.info等5个方法
    如果需要修改log_level，调用easylog.set_log_level，如果需要存入log文件，调用easylog.set_logger_storage_file方法
    不要直接使用logger_wrapper或是LoggerWrapper，否则可能出现不可预知的错误
    """
    default_stream_formatter = logging.Formatter(
                fmt='%(asctime)s \033[0;%(colorcode)sm[%(levelname)s]\033[0m >>> \033[0;%(colorcode)sm%(message)s\033[0m',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
    default_file_formatter = logging.Formatter(
                fmt='%(asctime)s [%(levelname)s] >>> %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )

    def __init__(self):
        self.singleton_logger = self.get_logger()

    def get_logger(
            self,
            logger_name="singleton_logger",  # 默认为单例模式
            log_file=None,
            level=logging.INFO,
            formatter=None
    ):
        """
        获取logger的方法。不要在任何模块中调用此方法，因为此方法已在本模块中调用。 # 最好将此类改为单例模式，更方便使用。
        :param logger_name: logger的名字
        :param log_file: 存储位置，默认不存储
        :param level: 进行显示的最低日志级别，默认为info
        :param formatter: 使用的logger格式，默认为类中的default_formatter
        :return:
        """
        # 设置格式
        if formatter is None:
            formatter = self.default_stream_formatter
        # 设置控制台处理器
        console_handler = logging.StreamHandler(stream=sys.stdout)
        console_handler.setFormatter(formatter)
        # 设置logger
        my_logger = logging.getLogger(logger_name)
        my_logger.setLevel(level)
        my_logger.addHandler(console_handler)
        my_logger.propagate = False
        # 设置文件处理器
        if log_file is not None:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            my_logger.addHandler(file_handler)
        my_logger.debug('my_logger设定完毕')
        return my_logger

    def update_kwargs(
            self,
            kwargs,
            color_code
    ):
        kwargs["extra"] = {}
        kwargs["extra"]["colorcode"] = color_code
        # 获取堆栈信息
        try:
            (fn, lno, func, _) = self.singleton_logger.findCaller()
            fn = os.path.basename(fn)
        except Exception:
            fn, lno, func = "(unknown file)", 0, "(unknown function)"
        kwargs["extra"]["myfn"] = fn
        kwargs["extra"]["mylno"] = lno
        kwargs["extra"]["myfunc"] = func
        kwargs["extra"]["mymodule"] = ""


# -------------------------------------- 静态方法 -------------------------------------- #
def save_info(
        save_file: str = 'info.log',  # 文件名
        save_level=logging.INFO,
        formatter=None
):
    """
    设置logger的存储位置
    :param save_file: 存储位置
    :param save_level: 存储级别
    :param formatter: 存储时的formatter
    :return:
    """
    # 清除之前的file_handler
    if len(logger_wrapper.singleton_logger.handlers) == 2:
        info("单例logger中已有file handler，正在清除旧的file handler，添加新的file handler")
        logger_wrapper.singleton_logger.removeHandler(logger_wrapper.singleton_logger.handlers[1])
    # 设置格式
    if formatter is None:
        formatter = logger_wrapper.default_file_formatter
    # 设置文件处理器
    file_handler = logging.FileHandler(filename=save_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(save_level)
    logger_wrapper.singleton_logger.addHandler(file_handler)
    info('logger文件设定完毕，log文件存储目标为%s' % save_file)


def save_warning(
        save_file: str = 'warning.log',  # 文件名
        save_level=logging.WARNING,
        formatter=None
):
    """
    设置logger的存储位置
    :param save_file: 存储位置
    :param save_level: 存储级别
    :param formatter: 存储时的formatter
    :return:
    """
    # 清除之前的file_handler
    if len(logger_wrapper.singleton_logger.handlers) == 2:
        info("单例logger中已有file handler，正在清除旧的file handler，添加新的file handler")
        logger_wrapper.singleton_logger.removeHandler(logger_wrapper.singleton_logger.handlers[1])
    # 设置格式
    if formatter is None:
        formatter = logger_wrapper.default_file_formatter
    # 设置文件处理器
    file_handler = logging.FileHandler(filename=save_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(save_level)
    logger_wrapper.singleton_logger.addHandler(file_handler)
    info('logger文件设定完毕，log文件存储目标为%s' % save_file)


def save_error(
        save_file: str = 'error.log',  # 文件名
        save_level=logging.ERROR,
        formatter=None
):
    """
    设置logger的存储位置
    :param save_file: 存储位置
    :param save_level: 存储级别
    :param formatter: 存储时的formatter
    :return:
    """
    # 清除之前的file_handler
    if len(logger_wrapper.singleton_logger.handlers) == 2:
        info("单例logger中已有file handler，正在清除旧的file handler，添加新的file handler")
        logger_wrapper.singleton_logger.removeHandler(logger_wrapper.singleton_logger.handlers[1])
    # 设置格式
    if formatter is None:
        formatter = logger_wrapper.default_file_formatter
    # 设置文件处理器
    file_handler = logging.FileHandler(filename=save_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(save_level)
    logger_wrapper.singleton_logger.addHandler(file_handler)
    info('logger文件设定完毕，log文件存储目标为%s' % save_file)


def set_log_level(
        log_level
):
    """
    设置console上显示的最低log等级
    :param log_level:
    :return:
    """
    if logger_wrapper.singleton_logger.hasHandlers():
        logger_wrapper.singleton_logger.handlers[0].setLevel(log_level)


def debug(
        message,
        *args,
        **kwargs
):
    """
    输出一条debug级别的日志
    :param message:
    :param args:
    :param kwargs:
    :return:
    """
    logger_wrapper.update_kwargs(kwargs, '36')  # 原色
    logger_wrapper.singleton_logger.debug(message, *args, **kwargs)


def info(
        message,
        *args,
        **kwargs
):
    logger_wrapper.update_kwargs(kwargs, '32')  # 绿色
    logger_wrapper.singleton_logger.info(message, *args, **kwargs)


def warning(
        message,
        *args,
        **kwargs
):
    logger_wrapper.update_kwargs(kwargs, '33')  # 黄色
    logger_wrapper.singleton_logger.warning(message, *args, **kwargs)


def error(
        message,
        *args,
        **kwargs
):
    logger_wrapper.update_kwargs(kwargs, '31')  # 红色
    logger_wrapper.singleton_logger.exception(message, *args, **kwargs)


def critical(
        message,
        *args,
        **kwargs
):
    logger_wrapper.update_kwargs(kwargs, '31')  # 红色
    logger_wrapper.singleton_logger.exception(message, *args, **kwargs)


logger_wrapper = LoggerWrapper()  # 实例化

if __name__ == '__main__':
    info('welcome to use showlog :)')
