# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name   :    decorators
   Description :
   Author      :    AlphaBrock
   date        :    2021/8/26
-------------------------------------------------
"""
import json
import logging
from functools import wraps

from rest_framework.response import Response

log = logging.getLogger("django.console")


def build_api_response(func):
    """Decorator for bundling and building API resource's response."""
    return_dict = {
        "status": True,
        "display_message": "",
        "result": [],
        "totalHits": 0
    }

    @wraps(func)
    def decorator(self, request, *args, **kwargs):
        status, result = func(self, request, *args, **kwargs)
        if not status:
            return_dict["status"] = False
            return_dict["display_message"] = result.get("result")
        else:
            return_dict["result"] = result.get("result")
            return_dict["totalHits"] = result.get("totalHits") if result.get("totalHits") else 0
        log.info(json.dumps(return_dict, ensure_ascii=False))
        return Response(return_dict)
    return decorator