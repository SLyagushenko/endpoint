
from rdflib import plugin, ConjunctiveGraph, Literal, URIRef
from rdflib.store import Store
from rdflib_sqlalchemy import registerplugins


class DBEngine:

    graph = ''

    def __init__(self):
        registerplugins()
        identifier = URIRef("rdfdb")
        cockroachdb_lit = 'cockroachdb://lab04:26257/rdfdb'
        sslmode = 'verify-full'
        sslcert = '/etc/cockroachdb/certs/client.root.crt'
        sslkey = '/etc/cockroachdb/certs/client.root.key'
        sslrootcert = '/etc/cockroachdb/certs/ca.crt'
        db_uri = Literal(cockroachdb_lit +
                         '?sslmode=' + sslmode +
                         '&sslcert=' + sslcert +
                         '&sslkey=' + sslkey +
                         '&sslrootcert=' + sslrootcert)
        store = plugin.get("SQLAlchemy", Store)(identifier=identifier,
                                                configuration=db_uri)
        self.graph = ConjunctiveGraph(store)
        self.graph.open(db_uri, create=True)

    def get_db_graph(self):
        return self.graph

    def graph_update(self, _graph):
        self.graph = _graph
