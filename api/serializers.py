# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name   :    serializers
   Description :
   Author      :    AlphaBrock
   date        :    2021/8/26
-------------------------------------------------
"""
from rest_framework import serializers
from api.models import RZY, V22, AIOPS, SIEM, KHZC


class RZYSerializer(serializers.ModelSerializer):
    class Meta:
        model = RZY
        fields = ('issuePrefix', 'issueTitle', 'issueType', 'issueStatus', 'issuePriority', 'issueResolution', 'issueAffectsVersions', 'issueComponents', 'issueFixVersions', 'issueLabels', 'issueDescription', 'issueAssignee', 'issueReporter', 'issueCreateTime', 'issueUpdateTime')

class V22Serializer(serializers.ModelSerializer):
    class Meta:
        model = V22
        fields = ('issuePrefix', 'issueTitle', 'issueType', 'issueStatus', 'issuePriority', 'issueResolution', 'issueAffectsVersions', 'issueComponents', 'issueFixVersions', 'issueLabels', 'issueDescription', 'issueAssignee', 'issueReporter', 'issueCreateTime', 'issueUpdateTime')


class AIOPSSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIOPS
        fields = ('issuePrefix', 'issueTitle', 'issueType', 'issueStatus', 'issuePriority', 'issueResolution', 'issueAffectsVersions', 'issueComponents', 'issueFixVersions', 'issueLabels', 'issueDescription', 'issueAssignee', 'issueReporter', 'issueCreateTime', 'issueUpdateTime')


class SIEMSerializer(serializers.ModelSerializer):
    class Meta:
        model = SIEM
        fields = ('issuePrefix', 'issueTitle', 'issueType', 'issueStatus', 'issuePriority', 'issueResolution', 'issueAffectsVersions', 'issueComponents', 'issueFixVersions', 'issueLabels', 'issueDescription', 'issueAssignee', 'issueReporter', 'issueCreateTime', 'issueUpdateTime')


class KHZCSerializer(serializers.ModelSerializer):
    class Meta:
        model = KHZC
        fields = ('issuePrefix', 'issueTitle', 'issueType', 'issueStatus', 'issuePriority', 'issueResolution', 'issueAffectsVersions', 'issueComponents', 'issueFixVersions', 'issueLabels', 'issueDescription', 'issueAssignee', 'issueReporter', 'issueCreateTime', 'issueUpdateTime')