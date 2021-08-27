# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name   :    model
   Description :
   Author      :    AlphaBrock
   date        :    2021/8/26
-------------------------------------------------
"""
from django.db import models


class RZY(models.Model):
    issuePrefix = models.IntegerField()
    issueTitle = models.CharField("标题", max_length=255)
    issueType = models.CharField("类型", max_length=60)
    issueStatus = models.CharField("状态", max_length=60)
    issuePriority = models.CharField("优先级", max_length=60)
    issueResolution = models.CharField("解决结果", max_length=60)
    issueAffectsVersions = models.CharField("影响版本", max_length=60)
    issueComponents = models.CharField("模块", max_length=60)
    issueFixVersions = models.CharField("修复的版本", max_length=60)
    issueLabels = models.CharField("标签", max_length=60)
    issueDescription = models.TextField("问题描述")
    issueAssignee = models.CharField("经办人", max_length=60)
    issueReporter = models.CharField("报告人", max_length=60)
    issueCreateTime = models.CharField("创建时间", max_length=60)
    issueUpdateTime = models.CharField("更新时间", max_length=60)
    createDate = models.DateTimeField(auto_created=True, auto_now_add=True)


class V22(models.Model):
    issuePrefix = models.IntegerField()
    issueTitle = models.CharField("标题", max_length=255)
    issueType = models.CharField("类型", max_length=60)
    issueStatus = models.CharField("状态", max_length=60)
    issuePriority = models.CharField("优先级", max_length=60)
    issueResolution = models.CharField("解决结果", max_length=60)
    issueAffectsVersions = models.CharField("影响版本", max_length=60)
    issueComponents = models.CharField("模块", max_length=60)
    issueFixVersions = models.CharField("修复的版本", max_length=60)
    issueLabels = models.CharField("标签", max_length=60)
    issueDescription = models.TextField("问题描述")
    issueAssignee = models.CharField("经办人", max_length=60)
    issueReporter = models.CharField("报告人", max_length=60)
    issueCreateTime = models.CharField("创建时间", max_length=60)
    issueUpdateTime = models.CharField("更新时间", max_length=60)
    createDate = models.DateTimeField(auto_created=True, auto_now_add=True)


class KHZC(models.Model):
    issuePrefix = models.IntegerField()
    issueTitle = models.CharField("标题", max_length=255)
    issueType = models.CharField("类型", max_length=60)
    issueStatus = models.CharField("状态", max_length=60)
    issuePriority = models.CharField("优先级", max_length=60)
    issueResolution = models.CharField("解决结果", max_length=60)
    issueAffectsVersions = models.CharField("影响版本", max_length=60)
    issueComponents = models.CharField("模块", max_length=60)
    issueFixVersions = models.CharField("修复的版本", max_length=60)
    issueLabels = models.CharField("标签", max_length=60)
    issueDescription = models.TextField("问题描述")
    issueAssignee = models.CharField("经办人", max_length=60)
    issueReporter = models.CharField("报告人", max_length=60)
    issueCreateTime = models.CharField("创建时间", max_length=60)
    issueUpdateTime = models.CharField("更新时间", max_length=60)
    createDate = models.DateTimeField(auto_created=True, auto_now_add=True)


class AIOPS(models.Model):
    issuePrefix = models.IntegerField()
    issueTitle = models.CharField("标题", max_length=255)
    issueType = models.CharField("类型", max_length=60)
    issueStatus = models.CharField("状态", max_length=60)
    issuePriority = models.CharField("优先级", max_length=60)
    issueResolution = models.CharField("解决结果", max_length=60)
    issueAffectsVersions = models.CharField("影响版本", max_length=60)
    issueComponents = models.CharField("模块", max_length=60)
    issueFixVersions = models.CharField("修复的版本", max_length=60)
    issueLabels = models.CharField("标签", max_length=60)
    issueDescription = models.TextField("问题描述")
    issueAssignee = models.CharField("经办人", max_length=60)
    issueReporter = models.CharField("报告人", max_length=60)
    issueCreateTime = models.CharField("创建时间", max_length=60)
    issueUpdateTime = models.CharField("更新时间", max_length=60)
    createDate = models.DateTimeField(auto_created=True, auto_now_add=True)


class SIEM(models.Model):
    issuePrefix = models.IntegerField()
    issueTitle = models.CharField("标题", max_length=255)
    issueType = models.CharField("类型", max_length=60)
    issueStatus = models.CharField("状态", max_length=60)
    issuePriority = models.CharField("优先级", max_length=60)
    issueResolution = models.CharField("解决结果", max_length=60)
    issueAffectsVersions = models.CharField("影响版本", max_length=60)
    issueComponents = models.CharField("模块", max_length=60)
    issueFixVersions = models.CharField("修复的版本", max_length=60)
    issueLabels = models.CharField("标签", max_length=60)
    issueDescription = models.TextField("问题描述")
    issueAssignee = models.CharField("经办人", max_length=60)
    issueReporter = models.CharField("报告人", max_length=60)
    issueCreateTime = models.CharField("创建时间", max_length=60)
    issueUpdateTime = models.CharField("更新时间", max_length=60)
    createDate = models.DateTimeField(auto_created=True, auto_now_add=True)
