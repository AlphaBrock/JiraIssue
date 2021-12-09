# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name   :    view
   Description :
   Author      :    AlphaBrock
   date        :    2021/8/26
-------------------------------------------------
"""
import json
import logging
from rest_framework.views import APIView
from JiraIssue.utils.decorators import build_api_response
from JiraIssue.utils.resource import MyUtils


log = logging.getLogger("django.console")


class Jira(APIView):

    results = {}

    def issueNotice(self, request, modelsType, serializer, **kwargs):
        try:
            limit = request.get("limit")
            if not limit:
                limit = 10
            result = serializer(modelsType.objects.all().order_by('-id')[0:int(limit)], many=True)
            self.results["result"] = result.data
            self.results["totalHits"] = len(result.data)
            return True, self.results
        except Exception as e:
            log.exception(str(e))
            return False, str(e)

    def issueSummary(self, request, modelsType, serializer, **kwargs):
        try:
            startIndex = request.get("startIndex")
            endIndex = request.get("endIndex")
            result = serializer(modelsType.objects.all().order_by('-id'), many=True)
            self.results["result"] = result.data[int(startIndex)-1:int(endIndex)]
            self.results["totalHits"] = len(result.data)
            return True, self.results
        except Exception as e:
            log.exception(str(e))
            return False, str(e)

    def issueSearch(self, request, modelsType, serializer, **kwargs):
        try:
            issueReporter = request.get("issueReporter")
            result = serializer(modelsType.objects.filter(issueReporter__contains=issueReporter), many=True)
            self.results["result"] = result.data
            self.results["totalHits"] = len(result.data)
            return True, self.results
        except Exception as e:
            log.exception(str(e))
            return False, str(e)

    def issueDetail(self, request, modelsType, serializer, **kwargs):
        issuePrefix = request.get("issuePrefix")
        try:
            result = serializer(modelsType.objects.filter(issuePrefix__contains=issuePrefix), many=True)
            self.results["result"] = result.data
            self.results["totalHits"] = len(result.data)
            return True, self.results
        except Exception as e:
            log.exception(str(e))
            return False, str(e)

    @build_api_response
    def get(self, request, **kwargs):
        global result, status

        log.info(json.dumps(kwargs))
        log.info(json.dumps(request.GET, ensure_ascii=False))

        if kwargs["jiraType"].upper() not in ["RZY", "V22", "AIOPS", "SIEM", "KHZC"]:
            return False, "哥, 你的URL有误, 检查下?"

        modelsType, serializer = MyUtils().getModelsObject(kwargs["jiraType"].upper())

        if kwargs["jiraAction"] == "notice":
            status, result = self.issueNotice(request.GET, modelsType, serializer)
        elif kwargs["jiraAction"] == "summary":
            status, result = self.issueSummary(request.GET, modelsType, serializer)
        elif kwargs["jiraAction"] == "search":
            status, result = self.issueSearch(request.GET, modelsType, serializer)
        elif kwargs["jiraAction"] == "detail":
            status, result = self.issueDetail(request.GET, modelsType, serializer)
        else:
            return False, "哥, 你的URL有误, 检查下?"

        return status, result

    @build_api_response
    def post(self, request, **kwargs):
        return False, "哥, 你的接口Method使用不对, 仅支持GET"

    @build_api_response
    def put(self, request, **kwargs):
        return False, "哥, 你的接口Method使用不对, 仅支持GET"

    @build_api_response
    def delete(self, request, **kwargs):
        return False, "哥, 你的接口Method使用不对, 仅支持GET"