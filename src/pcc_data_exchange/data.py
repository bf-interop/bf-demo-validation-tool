import json

from pyodide.http import open_url
import rdflib

SHACL = rdflib.Namespace("http://www.w3.org/ns/shacl#")

shacl_graph = rdflib.Graph()
shacl_graph.namespace_manager.bind("bf", "http://id.loc.gov/ontologies/bibframe/")
shacl_graph.namespace_manager.bind("bflc", "http://id.loc.gov/ontologies/bflc/")
shacl_graph.namespace_manager.bind("sinopia", "http://sinopia.io/vocabulary/")

def init_shacl_graph(shacl_urls: list) -> rdflib.Graph:
    """Initialize SHACL Graph"""
    for url in shacl_urls:
        result = open_url(url)
        json_ld = json.loads(result.getvalue())['data']
        graph = rdflib.Graph()
        graph.parse(data=json.dumps(json_ld), format='json-ld')
        shacl_graph.parse(data=graph.serialize(format='nt'))
    return shacl_graph