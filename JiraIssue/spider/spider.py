# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name   :    jiraIssueSpider
   Description :    爬取全量jira issue情况
   Author      :    jccia
   date        :    2021/8/10
-------------------------------------------------
"""
import json

import requests
from lxml import etree

from JiraIssue.utils.logger import Logger

log = Logger(loggeNname="spider")


class Jira(object):

    def __init__(self, BaseUrl, JiraUserName, JiraUserPasswd):
        self.BaseUrl = BaseUrl
        self.JiraUserName = JiraUserName
        self.JiraUserPasswd = JiraUserPasswd
        self.Headers = {
            'Host': self.BaseUrl,
            'Origin': 'https://{}'.format(self.BaseUrl),
            'X-Atlassian-Token': 'no-check',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
        }
        self.login()

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
                                            data=kwargs.get("payload"), allow_redirects=False, verify=False, timeout=60)
                if response.status_code == 200 or response.status_code == 302:
                    return response
                return None
            except Exception as e:
                log.logger.exception(json.dumps(kwargs, ensure_ascii=False) + "获取异常:[{}]".format(str(e)))
                return None

        try:
            response = requests.request(kwargs.get("method"), kwargs.get("url"), headers=kwargs.get("headers"),
                                        verify=False, timeout=60)
            if response.status_code == 200:
                return response
            return None
        except Exception as e:
            log.logger.exception(json.dumps(kwargs, ensure_ascii=False) + "获取异常:[{}]".format(str(e)))
            return None

    def login(self):
        """
        模拟登陆获取Cookie
        :return:
        """
        url = "https://{}/login.jsp".format(self.BaseUrl)
        self.Headers["Referer"] = url
        self.Headers["Content-Type"] = "application/x-www-form-urlencoded"

        payload = {
            "os_username": self.JiraUserName,
            "os_password": self.JiraUserPasswd,
            "os_destination": "",
            "user_role": "",
            "atl_token": "",
            "login": "登陆"
        }
        result = self.httpRequests(url=url, method="POST", payload=payload, headers=self.Headers)
        cookieJsessionId = result.headers["Set-Cookie"].split(";")[0]

        url = "https://{}".format(self.BaseUrl)
        result = self.httpRequests(url=url, method="GET", headers=self.Headers)
        cookieToken = result.headers["Set-Cookie"].split(";")[0].replace("lout", "lin")
        self.Headers["Cookie"] = cookieJsessionId+";"+cookieToken

    def getIssueLists(self, jql: str, filterId: str):
        """
        按照条件筛选Issue
        :return:
        """
        url = "https://{}/rest/issueNav/1/issueTable".format(self.BaseUrl)
        self.Headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
        self.Headers["Referer"] = "https://{}/issues/?jql=project%20%3D%20RZY".format(self.BaseUrl)
        payload = {
            "startIndex": 0,
            # "jql": 'project = RZY AND status in (Open, "In Progress", Reopened, "To Do", "In Review") order by priority DESC,updated DESC',
            "jql": jql,
            "filterId": filterId,
            "layoutKey": "split-view"
        }

        result = json.loads(self.httpRequests(url=url, method="POST", payload=payload, headers=self.Headers).text)
        if result:
            issueKeys = result["issueTable"]["issueKeys"]
            return issueKeys

    def getIssueHtmlData(self, issueKey: str) -> dict:
        """
        获取单个Issue详情
        :return:
        """
        url = "https://{}/browse/RZY-{}".format(self.BaseUrl, issueKey)
        log.logger.debug("issueKey:{}".format(url))
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
                                                                                                       "").replace(
            "\xa0", "")
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
        issueUpdateTime = "".join(parseHtml.xpath('//*[@id="updated-val"]/time/@datetime')).replace("\n",
                                                                                                    "").replace(
            " ", "")
        issueData = {"URL": url, "issueTitle": issueTitle, "issueType": issueType, "issueStatus": issueStatus, "issuePriority": issuePriority,
                     "issueResolution": issueResolution, "issueAffectsVersions": issueAffectsVersions, "issueFixVersions": issueFixVersions,
                     "issueComponents": issueComponents, "issueLabels": issueLabels, "issueDescription": issueDescription, "issueAssignee": issueAssignee,
                     "issueReporter": issueReporter, "issueCreateTime": issueCreateTime, "issueUpdateTime": issueUpdateTime}

        log.logger.info(json.dumps(issueData, ensure_ascii=False))
        return issueData