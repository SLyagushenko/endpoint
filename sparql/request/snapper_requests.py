import io
import json
from rdflib import Graph
from sparql.request.db_engine import DBEngine
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from rdflib.plugins.sparql.results import jsonresults


class SnapperRequests:

    graph = ''
    accept_types = ['application/json',
                    'text/turtle',
                    'application/sparql-results+json']

    def __init__(self):
        db = DBEngine()
        self.graph = db.get_db_graph()

    def refer(self, request, query, http_accept):
        if request.method == 'GET':
            if self.accept_types[2] in http_accept:
                _json = self.snapper_sparql_request(request.GET.get('query'))
                response = JsonResponse(_json,
                                        content_type=self.accept_types[1])
                response['Content-Length'] = len(json.dumps(_json))
            else:
                response = HttpResponseForbidden('Snapper: 403 Forbidden')
        elif request.method == 'POST':
            if self.accept_types[0] in http_accept:
                if 'graph' in request.get_full_path():
                    self.snapper_insert_ttl(query)
                    response = HttpResponse('Snapper: Graph Updated')
                else:
                    _json = json.loads('{}')
                    response = JsonResponse(_json,
                                            content_type=self.accept_types[0])
                    response['Content-Length'] = len(json.dumps(_json))
            else:
                response = HttpResponseForbidden('Snapper: 403 Forbidden')
        elif request.method == 'PUT':
            if self.accept_types[0] in http_accept:
                self.snapper_repalce_graph(query)
                print(request.GET.get('query'))
                response = HttpResponse('Snapper: Graph Replaced')
            else:
                response = HttpResponseForbidden('Snapper: 403 Forbidden')
        else:
            response = HttpResponseForbidden('Snaper: 403 Forbidden')
        return response

    def snapper_insert_ttl(self, query):
        tmpgraph = Graph()
        tmpgraph.parse(data=query, encoding='utf-8', format='turtle')
        for t in tmpgraph:
            self.graph.add(t)
        db = DBEngine()
        db.graph_update(self.graph)

    def snapper_repalce_graph(self, query):
        self.graph.remove((None, None, None))
        self.snapper_insert_ttl(query)

    def snapper_sparql_request(self, query):
        result = io.StringIO()
        temp_result = self.graph.query(query)
        serial = jsonresults.JSONResultSerializer(temp_result)
        serial.serialize(result)
        _json = result.getvalue()
        result.close()
        _json = json.loads(_json)
        return _json
