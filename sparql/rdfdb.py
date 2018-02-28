import io
import json
from rdflib import plugin, ConjunctiveGraph, Literal, URIRef
from rdflib.store import Store
from rdflib.plugins.sparql.results import csvresults, jsonresults, tsvresults, xmlresults
from rdflib_sqlalchemy import registerplugins

class RDFdb:

    graph = ''

    def __init__(self):
        registerplugins()
        identifier = URIRef("rdfdb")
        db_uri = Literal('cockroachdb://lab04:26257/rdfdb?sslmode=verify-full&sslcert=/etc/cockroachdb/certs/client.root.crt&sslkey=/etc/cockroachdb/certs/client.root.key&sslrootcert=/etc/cockroachdb/certs/ca.crt')
        store = plugin.get("SQLAlchemy", Store)(identifier=identifier, configuration=db_uri)
        self.graph = ConjunctiveGraph(store)
        self.graph.open(db_uri, create=True)

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