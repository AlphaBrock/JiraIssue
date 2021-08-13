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


class Log(object):
    '''
   封装后的logging
    '''

    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }

    def __init__(self, logger=None, logname="jiraIssue.log", loglevel="debug"):
        '''
         指定保存日志的文件路径，日志级别，以及调用文件
         将日志存入到指定的文件中
        '''
        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(self.level_relations.get(loglevel))
        # 创建一个handler，用于写入日志文件

        fh = handlers.RotatingFileHandler(filename=logname, maxBytes=104857600, backupCount=6, encoding='utf-8')
        fh.setLevel(self.level_relations.get(loglevel))

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(self.level_relations.get(loglevel))

        # 定义handler的输出格式
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(filename)s:%(module)s.%(funcName)s:%(lineno)d] [%(process)d] [%(threadName)s] %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

        # 添加下面一句，在记录日志之后移除句柄
        # self.logger.removeHandler(ch)
        # self.logger.removeHandler(fh)
        # 关闭打开的文件
        fh.close()
        ch.close()

    def getLog(self):
        return self.logger
