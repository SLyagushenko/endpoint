# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.http import HttpResponse, JsonResponse, QueryDict, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.template import Context, loader, RequestContext
from sparql import rdfdb

request_types = ['application/sparql-results+json', 'application/sparql-results+xml', 'text/csv', 'text/tab-separated-values']

@csrf_exempt
def index(request):
    http_accept = request.META.get('HTTP_ACCEPT')
    if any(request_type in http_accept for request_type in request_types):
        if request.method == 'GET':    
            return HttpResponse('GET Not Implemented')

        elif request.method == 'POST':        
            q = QueryDict(request.body)
            query = list(q.items())[0][1]        
            db = rdfdb.RDFdb()
            if request_types[0] in http_accept:
                _json = db.get_result_json(query)
                response =  JsonResponse(_json, content_type = request_types[0])
                response['Content-Length'] = len(json.dumps(_json))
            elif request_types[1] in http_accept:
                _xml = db.get_result_xml(query)
                response = HttpResponse(_xml, content_type = request_types[1])
                response['Content-Length'] = len(_xml)
            elif request_types[2] in http_accept:
                _csv = db.get_result_csv(query)
                response = HttpResponse(_csv, content_type = request_types[2])
                response['Content-Length'] = len(_csv)
            elif request_types[3] in http_accept:
                response = HttpResponseForbidden('TSV Not Implemented')
            else:
                #db.update_graph(query)
                #response = HttpResponse('Graph Update Done!')
                response = HttpResponseForbidden('403 Forbidden')
            return response
    else:
        return HttpResponseForbidden('403 Forbidden')

    return HttpResponseForbidden('Not Implemented')