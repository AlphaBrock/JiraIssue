# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name   :    runner
   Description :
   Author      :    AlphaBrock
   date        :    2021/8/12
-------------------------------------------------
"""
import time
from pymysql.converters import escape_string
from JiraIssue.spider.spider import Jira
from JiraIssue.utils.sqlite3 import Database
from JiraIssue.utils.logger import Log

log = Log('__name__').getLog()

db = Database()


class Runner(Jira):
    issueType = {
        "日志易RZY": "RZY",
        "版本开发V22": "V22",
        "SIEM": "SIEMTRACE",
        "SIEM产品": "SIEM",
        "智能运维": "AIOPS",
        "客户支持": "KHZC"
    }

    issueFilter = {
        "打开问题": "resolution = Unresolved order by priority DESC,updated DESC",
        "最近创立": "created >= {} order by created DESC",
        "最近解决": "resolutiondate >= {} order by updated DESC",
        "最近更新": "updated >= {} order by updated DESC"
    }

    times = {
        "周": "w",
        "天": "d",
        "时": "h",
        "分": "m"
    }

    def __init__(self):
        super().__init__("jira.rizhiyi.com:8443", "chen.fei", "1qaz@WSX")

    def a(self):
        for issueKey in range(1, 7600):
            try:
                issueData = self.getIssueHtmlData(str(issueKey))
                sql = '''insert into RZY (issuePrefix, issueTitle, issueType, issueStatus, issuePriority, issueResolution, issueAffectsVersions, issueComponents, issueFixVersions, issueLabels, issueDescription, issueAssignee, issueReporter, issueCreateTime, issueUpdateTime) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')''' % ("RZY-"+str(issueKey), issueData.get("issueTitle"), issueData.get("issueType"), issueData.get("issueStatus"), issueData.get("issuePriority"), issueData.get("issueResolution"), issueData.get("issueAffectsVersions"), issueData.get("issueComponents"), issueData.get("issueFixVersions"), issueData.get("issueLabels"), escape_string(issueData.get("issueDescription")), issueData.get("issueAssignee"), issueData.get("issueReporter"), issueData.get("issueCreateTime"), issueData.get("issueUpdateTime"))
                # db.insert(sql)
                log.info(sql)
            except Exception as e:
                log.exception(str(e))
            finally:
                time.sleep(1)


if __name__ == '__main__':
    ru =Runner()
    ru.a()
