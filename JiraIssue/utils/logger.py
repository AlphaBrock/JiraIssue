# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name   :    logger
   Description :
   Author      :    jccia
   date        :    2021/8/11
-------------------------------------------------
"""
import logging
import os
from logging import handlers

if not os.path.exists("log"):
   os.mkdir("log")


class Logger(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }

    def __init__(self, logname="jiraIssue.log", loggeNname=None, loglevel="debug"):
        """
            即在终端打印也在文件打印
        """
        self.logger = logging.getLogger(loggeNname)
        self.logger.setLevel(self.level_relations.get(loglevel))
        fh = handlers.RotatingFileHandler(filename=logname, maxBytes=104857600, backupCount=6, encoding='utf-8')
        fh.setLevel(self.level_relations.get(loglevel))
        ch = logging.StreamHandler()
        ch.setLevel(self.level_relations.get(loglevel))
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(filename)s:%(module)s.%(funcName)s:%(lineno)d] [%(process)d] [%(threadName)s] %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
