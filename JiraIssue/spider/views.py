# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name   :    runner
   Description :
   Author      :    AlphaBrock
   date        :    2021/8/12
-------------------------------------------------
"""
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_job
from JiraIssue.spider.spider import Jira
from api.models import RZY, V22, AIOPS, SIEM, KHZC
from api.serializers import RZYSerializer, V22Serializer, AIOPSSerializer, SIEMSerializer, KHZCSerializer

log = logging.getLogger("django.console")
scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default", replace_existing=True)

JiraSpider = Jira()


class Scheduler(object):
    pass


try:
    @register_job(scheduler, 'cron', hour='11', minute='0', second='1', misfire_grace_time=3600, id=None)
    def RZYJob():
        log.info("start to running schedule!")
        try:
            result = RZYSerializer(RZY.objects.all().order_by("-id")[0], many=True)
            startIndex = result.data.get("issuerefix") - 400
            endIndex = startIndex + 100
            JiraSpider.spider(startIndex, endIndex)
        except Exception as e:
            JiraSpider.spider(1, 8000)

    scheduler.start()
except Exception as e:
    log.exception(str(e))
    scheduler.shutdown()


