# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name   :    sqlite3
   Description :
   Author      :    jccia
   date        :    2021/8/11
-------------------------------------------------
"""
import sqlite3
import threading
import JiraIssue.utils.readSetting
from JiraIssue.utils.logger import Logger

sqliteMutex = threading.Lock()

log = Logger(logname="db")


class Database(object):

    def __init__(self):
        pass
        # super(Database, self).__init__()

    def initDb(self, dbTable: str):
        con = sqlite3.connect(self.dbPath)
        sql = '''CREATE TABLE IF NOT EXISTS %s
                (
                  id  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                  videoId    VARCHAR(20),
                  videoTitle    VARCHAR(20),
                  videoUrl    VARCHAR(20),
                  videoDuration VARCHAR(20),
                  videoPic   VARCHAR(20),
                  date TIMESTAMP NOT NULL DEFAULT (datetime('now','localtime'))
                );
        ''' % dbTable

        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        con.close()

    def select(self, sql):
        """
        select 操作，加锁防止deadlock
        :param sql:
        :return:
        """
        with sqliteMutex:
            con = sqlite3.connect("C:\github\JiraIssue\db.sqlite3")
            cur = con.cursor()
            cur.execute(sql)
            con.close()
            return cur

    def insert(self, sql):
        """
        insert 操作，加锁防止deadlock
        :param sql:
        :return:
        """
        with sqliteMutex:
            con = sqlite3.connect("C:\github\JiraIssue\db.sqlite3")
            cur = con.cursor()
            try:
                cur.execute(sql)
                con.commit()
            except Exception as e:
                log.logger.exception("sql:{}, 运行异常:{}".format(sql, e))
                con.rollback()
            finally:
                con.close()