# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name   :    jiraIssueSpider
   Description :    爬取全量jira issue情况
   Author      :    jccia
   date        :    2021/8/10
-------------------------------------------------
"""
import requests
import json
import csv
import time
from lxml import etree
import logging
from logging import handlers
from JiraIssue.utils.logger import Logger

logger = Logger(loggeNname="spider")


class Jira(object):

    def __init__(self):
        self.BaseUrl = "jira.rizhiyi.com:8443"
        self.Headers = {
            'Host': self.BaseUrl,
            'Origin': 'https://{}'.format(self.BaseUrl),
            'Cookie': Cookie,
            'X-Atlassian-Token': 'no-check',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
            # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }

    @staticmethod
    def parseResults(html):

        try:
            html = etree.HTML(html, etree.HTMLParser())
            return html
        except Exception as e:
            log.logger.exception(str(e))
            return None

    @staticmethod
    def httpRequests(**kwargs):
        if kwargs.get("payload"):
            try:
                response = requests.request(kwargs.get("method"), kwargs.get("url"), headers=kwargs.get("headers"),
                                            data=kwargs.get("payload"), verify=False, timeout=60)
                if response.status_code == 200:
                    return json.loads(response.text)
                return None
            except Exception as e:
                log.logger.exception(json.dumps(kwargs, ensure_ascii=False) + "获取异常:[{}]".format(str(e)))
                return None

        try:
            response = requests.request(kwargs.get("method"), kwargs.get("url"), headers=kwargs.get("headers"),
                                        verify=False, timeout=60)
            if response.status_code == 200:
                # return json.loads(response.text)
                return response.text
            return None
        except Exception as e:
            log.logger.exception(json.dumps(kwargs, ensure_ascii=False) + "获取异常:[{}]".format(str(e)))
            return None

    def getIssueLists(self):
        url = "https://{}/rest/issueNav/1/issueTable".format(self.BaseUrl)
        self.Headers["Cookie"] = Cookie
        self.Headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
        self.Headers["Referer"] = "https://{}/issues/?jql=project%20%3D%20RZY".format(self.BaseUrl)
        payload = {
            "startIndex": 0,
            "jql": 'project = RZY AND status in (Open, "In Progress", Reopened, "To Do", "In Review") order by priority DESC,updated DESC',
            "filterId": "-5",
            "layoutKey": "split-view"
        }
        result = self.httpRequests(url=url, method="POST", payload=payload, headers=self.Headers)
        if result:
            issueKeys = result["issueTable"]["issueKeys"]
            return issueKeys

    def getIssueHtmlData(self):
        # issueKeys = self.getIssueLists()
        # del self.Headers["Referer"]
        # del self.Headers["Content-Type"]
        self.Headers["Cookie"] = Cookie
        with open("jiraIssueData.csv", "a+", encoding='utf-8') as csv_file:
            fieldnames = ["URL", "标题", "类型", "状态", "优先级", "解决结果", "影响版本", "修复的版本", "模块", "标签", "描述", "经办人", "报告人",
                          "创建时间"]
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames, quoting=csv.QUOTE_ALL, escapechar='\\',
                                        quotechar='"')
            csv_writer.writeheader()
            # for issueKey in issueKeys:
            for issueKey in range(1, 7500):
                url = "https://{}/browse/RZY-{}".format(self.BaseUrl, issueKey)
                log.logger.debug("issueKey:{}".format(url))
                try:
                    result = self.httpRequests(url=url, method="GET", headers=self.Headers)
                    parseHtml = self.parseResults(result)

                    issueTitle = parseHtml.xpath(
                        "//header[contains(@class, 'aui-page-header')]/div[contains(@class, 'aui-page-header-inner')]/div[contains(@class, 'aui-page-header-main')]/h1/text()")[
                        0]

                    # issue详情
                    issueType = "".join(parseHtml.xpath('//*[@id="type-val"]/text()')).replace("\n", "").replace(" ", "")
                    issueStatus = "".join(parseHtml.xpath('//*[@id="status-val"]/span/text()')).replace("\n", "").replace(
                        " ", "")
                    issuePriority = "".join(parseHtml.xpath('//*[@id="priority-val"]/text()')).replace("\n", "").replace(
                        " ", "")
                    issueResolution = "".join(parseHtml.xpath('//*[@id="resolution-val"]/text()')).replace("\n",
                                                                                                           "").replace(" ",
                                                                                                                       "")
                    issueAffectsVersions = "".join(parseHtml.xpath('//*[@id="versions-val"]/text()')).replace("\n",
                                                                                                              "").replace(
                        " ", "")
                    if issueAffectsVersions == "":
                        issueAffectsVersions = "".join(parseHtml.xpath('//*[@id="versions-field"]/span/text()')).replace(
                            "\n", "").replace(" ", "")
                    issueComponents = "".join(parseHtml.xpath('//*[@id="components-field"]/a/text()')).replace("\n",
                                                                                                               "").replace(
                        " ", "")
                    issueFixVersions = "".join(parseHtml.xpath('//*[@id="fixfor-val"]/text()')).replace("\n", "").replace(
                        " ", "")
                    issueLabels = "".join(
                        parseHtml.xpath('//*[@id="wrap-labels"]/div[contains(@class,"labels-wrap value")]/span/text()'))

                    # issue描述
                    issueDescription = "\n".join(parseHtml.xpath('//*[@id="description-val"]/div/text()')).replace("<br>",
                                                                                                                   "").replace("\xa0", "")
                    # issueDescription = ""

                    # issue人员
                    issueAssignee = "".join(parseHtml.xpath('//*[@id="assignee-val"]/span/text()')).replace("\n",
                                                                                                            "").replace(" ",
                                                                                                                        "")
                    issueReporter = "".join(parseHtml.xpath('//*[@id="reporter-val"]/span/text()')).replace("\n",
                                                                                                            "").replace(" ",
                                                                                                                        "")

                    # issue日期
                    issueCreateTime = "".join(parseHtml.xpath('//*[@id="created-val"]/time/@datetime')).replace("\n",
                                                                                                                "").replace(
                        " ", "")
                    issueData = {"URL": url, "标题": issueTitle, "类型": issueType, "状态": issueStatus, "优先级": issuePriority,
                                 "解决结果": issueResolution, "影响版本": issueAffectsVersions, "修复的版本": issueFixVersions,
                                 "模块": issueComponents, "标签": issueLabels, "描述": issueDescription, "经办人": issueAssignee,
                                 "报告人": issueReporter, "创建时间": issueCreateTime}

                    log.logger.info(json.dumps(issueData, ensure_ascii=False))
                    csv_writer.writerow(issueData)
                except Exception as e:
                    log.logger.exception(str(e))
                finally:
                    time.sleep(1)


if __name__ == '__main__':
    log = Logger()
    Cookie = "_ga=GA1.2.331566738.1611638722; Hm_lvt_7b79eb9425c1aa6c616a82083aee4a4d=1615722075,1617012806; JSESSIONID=A92C6181B0ED12CB260082D344D34305; atlassian.xsrf.token=BXV3-HF5O-JMT0-SJH5_b016ad37d4e8e6d19174953c9ca02b63a16a8711_lin"
    jira = Jira()
    jira.getIssueHtmlData()
