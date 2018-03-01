import io
import json
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from rdflib.plugins.sparql.results import csvresults, jsonresults, xmlresults
from sparql.request.db_engine import DBEngine


class YasguiRequests:

    graph = ''
    accept_types = ['application/sparql-results+json',
                    'application/sparql-results+xml',
                    'text/csv',
                    'text/tab-separated-values',
                    'text/plain']

    def __init__(self):
        db = DBEngine()
        self.graph = db.get_db_graph()

    def refer(self, request, query, http_accept):
        if request.method == 'GET':
            print('YASGUI: GET: ' + request.GET.get('query'))
            return HttpResponse('YASGUI: GET Not Implemented')

        elif request.method == 'POST':
            if self.accept_types[0] in http_accept:
                _json = self.get_result_json(query[0][1])
                response = JsonResponse(_json,
                                        content_type=self.accept_types[0])
                response['Content-Length'] = len(json.dumps(_json))
            elif self.accept_types[1] in http_accept:
                _xml = self.get_result_xml(query[0][1])
                response = HttpResponse(_xml,
                                        content_type=self.accept_types[1])
                response['Content-Length'] = len(_xml)
            elif self.accept_types[2] in http_accept:
                _csv = self.get_result_csv(query[0][1])
                response = HttpResponse(_csv,
                                        content_type=self.accept_types[2])
                response['Content-Length'] = len(_csv)
            elif self.accept_types[3] in http_accept:
                response = HttpResponseForbidden('YASGUI: TSV Not Implemented')
            elif self.accept_types[4] in http_accept:
                self.update_graph(query[0][1])
                response = HttpResponse('YASGUI: Graph Update Done!')
            else:
                response = HttpResponseForbidden('YASGUI: 403 Forbidden')
            return response

    def get_result_json(self, query):
        result = io.StringIO()
        temp_result = self.graph.query(query)
        serial = jsonresults.JSONResultSerializer(temp_result)
        serial.serialize(result)
        _json = result.getvalue()
        result.close()
        _json = json.loads(_json)
        return _json

    def get_result_xml(self, query):
        result = io.BytesIO()
        temp_result = self.graph.query(query)
        serializer = xmlresults.XMLResultSerializer(temp_result)
        serializer.serialize(result)
        _xml = result.getvalue()
        result.close()
        return _xml

    def get_result_csv(self, query):
        result = io.BytesIO()
        temp_result = self.graph.query(query)
        serializer = csvresults.CSVResultSerializer(temp_result)
        serializer.serialize(result)
        _csv = result.getvalue()
        result.close()
        return _csv

    def update_graph(self, query):
        self.graph.update(query)
        db = DBEngine()
        db.graph_update(self.graph)
