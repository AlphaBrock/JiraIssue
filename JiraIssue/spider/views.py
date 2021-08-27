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
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.triggers.cron import CronTrigger
from django.db.models import Q
from django_apscheduler.jobstores import DjangoJobStore, register_job
from JiraIssue.spider.spider import Jira
from JiraIssue.utils.resource import MyUtils
from api.models import RZY, V22, AIOPS, SIEM, KHZC
from api.serializers import RZYSerializer, V22Serializer, AIOPSSerializer, SIEMSerializer, KHZCSerializer

log = logging.getLogger("django.spider")

executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(10)
}
scheduler = BackgroundScheduler(executors=executors)
scheduler.add_jobstore(DjangoJobStore(), "default", replace_existing=True)

JiraSpider = Jira()


class Scheduler(object):
    pass


try:
    @register_job(scheduler, CronTrigger.from_crontab(MyUtils().getConfig().get("FullScanJira")), misfire_grace_time=3600, id=None)
    def FullScanJiraJob():
        log.info("start to running full scan Job!")
        try:
            result = RZYSerializer(RZY.objects.all().order_by("-id")[0], many=True)
            startIndex = result.data.get("issuerefix") - 400
            endIndex = startIndex + 100
            JiraSpider.FullScanJiraJob(startIndex, endIndex)
        except Exception as e:
            JiraSpider.FullScanJiraJob(1, 20)
        log.info("finished the full scan Job!")

    @register_job(scheduler, CronTrigger.from_crontab(MyUtils().getConfig().get("FullUpdateJira")), misfire_grace_time=3600, id=None)
    def FullUpdateJiraJob():
        log.info("start to running full update Job!")
        try:
            result = RZYSerializer(RZY.objects.exclude(Q(issueStatus="已关闭") | Q(issueStatus="已解决")), many=True)
            log.info("当前{}个Issue需要更新".format(len(result.data)))
            JiraSpider.FullUpdateJiraJob(result.data)
        except Exception as e:
            log.warning("当前无Issue需要更新")
        log.info("finished the full update Job!")

    scheduler.start()
except Exception as e:
    log.exception(str(e))
    scheduler.shutdown()


