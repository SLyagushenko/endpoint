# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, JsonResponse
from django.http import QueryDict, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from sparql.request import snapper_requests, yasgui_requests

referers = ['/yasgui/',
            '/snapper/']


@csrf_exempt
def index(request):
    http_referer = request.META.get('HTTP_REFERER')
    http_accept = request.META.get('HTTP_ACCEPT')

    if any(refer in http_referer for refer in referers):
        if referers[0] in http_referer:
            query = list(QueryDict(request.body).items())
            _yasgui = yasgui_requests.YasguiRequests()
            return _yasgui.refer(request, query, http_accept)
        elif referers[1] in http_referer:
            query = request.body.decode("utf-8")
            _snapper = snapper_requests.SnapperRequests()
            return _snapper.refer(request, query, http_accept)
        else:
            return HttpResponseForbidden('403 Forbidden2')
    else:
        return HttpResponseForbidden('403 Forbidden3')
