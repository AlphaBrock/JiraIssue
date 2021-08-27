# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name   :    resource
   Description :
   Author      :    AlphaBrock
   date        :    2021/8/27
-------------------------------------------------
"""
from api.models import RZY, V22, AIOPS, SIEM, KHZC
from api.serializers import RZYSerializer, V22Serializer, AIOPSSerializer, SIEMSerializer, KHZCSerializer


class MyUtils(object):

    def getModelsObject(self, JiraType):
        global modelsType, serializer
        JiraType = JiraType
        if JiraType == "RZY":
            modelsType = RZY
            serializer = RZYSerializer
        elif JiraType == "V22":
            modelsType = V22
            serializer = V22Serializer
        elif JiraType == "AIOPS":
            modelsType = AIOPS
            serializer = AIOPSSerializer
        elif JiraType == "SIEM":
            modelsType = SIEM
            serializer = SIEMSerializer
        elif JiraType == "KHZC":
            modelsType = KHZC
            serializer = KHZCSerializer
        return modelsType, serializer