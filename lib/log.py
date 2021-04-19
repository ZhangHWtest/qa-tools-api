#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import env
from datetime import datetime


class Log(object):
    def __init__(self, name):
        check_path = '.'
        log_path = os.path.join(check_path, 'log')
        if not os.path.exists(log_path):
            os.mkdir(log_path)
        self.name = name
        strtime = datetime.now().strftime("%m%d%H%M")
        self.filename = os.path.join(log_path, "%s_%s.log" % (self.name, strtime))
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.DEBUG)
    
    def get_file_logger(self):
        handler = logging.FileHandler(self.filename)
        handler.setLevel(env.log_level)
        formatter = logging.Formatter("[%(asctime)s] [%(lineno)d] %(levelname)s %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        return self.logger
            
    def get_stream_logger(self):
        handler = logging.StreamHandler()
        handler.setLevel(env.log_level)
        formatter = logging.Formatter("[%(asctime)s] [%(lineno)d] %(levelname)s %(message)s", '%Y-%m-%d %H:%M:%S')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        return self.logger


if __name__ == "__main__":
    logger = Log("zatest").get_stream_logger()
    logger.debug("test debug")
    logger.info("test info")
    logger.error("test error")
    logger.warning("test warning")
    logger.critical("test critical")
