#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging


class MyLogger(object):
    """日志模块，这里会记录测试的日志。"""
    def __init__(self, title, filename):
        self.logger = logging.Logger(title)
        self.logger.setLevel(logging.INFO)
        self.filename = filename
        self.formatter = '[%(asctime)s][%(name)s:%(funcName)s:%(lineno)d][%(levelname)s][%(thread)d] - %(message)s'

    def get_both_logger(self):
        logfile = logging.FileHandler(self.filename)
        logfile.setLevel(logging.INFO)
        control = logging.StreamHandler()
        control.setLevel(logging.INFO)
        fmt = logging.Formatter(self.formatter)
        logfile.setFormatter(fmt)
        control.setFormatter(fmt)
        self.logger.addHandler(logfile)
        self.logger.addHandler(control)
        return self.logger

    def get_file_logger(self):
        logfile = logging.FileHandler(self.filename)
        logfile.setLevel(logging.INFO)
        fmt = logging.Formatter(self.formatter)
        logfile.setFormatter(fmt)
        self.logger.addHandler(logfile)
        return self.logger

    def get_stream_logger(self):
        control = logging.StreamHandler()
        control.setLevel(logging.INFO)
        fmt = logging.Formatter(self.formatter)
        control.setFormatter(fmt)
        self.logger.addHandler(control)
        return self.logger
