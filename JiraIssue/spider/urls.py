# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name   :    urls
   Description :
   Author      :    AlphaBrock
   date        :    2021/8/26
-------------------------------------------------
"""
from django.urls import re_path

from JiraIssue.spider import views

urlpatterns = [
    re_path(r'^$', views.Scheduler)
]