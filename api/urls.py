# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name   :    urls
   Description :
   Author      :    AlphaBrock
   date        :    2021/8/26
-------------------------------------------------
"""
from django.urls import re_path,path
from api.views import Jira

urlpatterns = [
    path('api/', Jira.as_view()),
    re_path(r'^api/(?P<jiraType>[^\/]+)/(?P<jiraAction>[^\/]+)$', Jira.as_view())
]