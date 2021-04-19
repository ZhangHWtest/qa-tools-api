#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging


class MyLogger(object):
	"""日志模块，这里会记录测试的日志。"""
	def __init__(self, title, filename):
		self.logger = logging.Logger(title)
		self.logger.setLevel(logging.INFO)
		self.logfile = logging.FileHandler(filename)
		self.logfile.setLevel(logging.INFO)
		self.control = logging.StreamHandler()
		self.control.setLevel(logging.INFO)
		formatter = '[%(asctime)s][%(name)s:%(module)s:%(funcName)s:%(lineno)d][%(levelname)s][%(thread)d] - %(message)s'
		self.fmt = logging.Formatter(formatter)
		self.logfile.setFormatter(self.fmt)
		self.control.setFormatter(self.fmt)
		self.logger.addHandler(self.logfile)
		self.logger.addHandler(self.control)

	def debug_log(self, message):
		self.logger.debug(message)

	def info_log(self, message):
		self.logger.info(message)

	def warn_log(self, message):
		self.logger.warning(message)

	def error_log(self, message):
		self.logger.error(message)
