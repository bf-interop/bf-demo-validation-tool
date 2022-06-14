import json

from pyodide.http import open_url
import rdflib

BF = rdflib.Namespace("http://id.loc.gov/ontologies/bibframe/")
BFLC = rdflib.Namespace("http://id.loc.gov/ontologies/bflc/")
SHACL = rdflib.Namespace("http://www.w3.org/ns/shacl#")
SINOPIA = rdflib.Namespace("http://sinopia.io/vocabulary/")

def _bind_namespaces(graph: rdflib.Graph):
    graph.namespace_manager.bind("bf", BF)
    graph.namespace_manager.bind("bflc", BFLC)
    graph.namespace_manager.bind("sinopia",SINOPIA)

def _build_from_urls(rdf_urls: str, incoming_graph: rdflib.Graph):
    urls = rdf_urls.split(",")
    for url in urls:
        if url.startswith("http://"):
            url = url.replace("http://", "https://")
        result = open_url(url.strip())
        if "sinopia" in url:
            sinopia_json_ld = json.loads(result.getvalue())['data']
            incoming_graph.parse(
                data=json.dumps(sinopia_json_ld), 
                format='json-ld')
        else:

            # Tries to guess parser type based on file
            rdf_type = rdflib.util.guess_format(url)
            raw_rdf = result.getvalue()
            incoming_graph.parse(
                data=raw_rdf,
                format=rdf_type
            )

def init_shacl_graph(shacl_urls: list) -> rdflib.Graph:
    """Initialize SHACL Graph"""
    shacl_graph = rdflib.Graph()
    _bind_namespaces(shacl_graph)
    for url in shacl_urls:
        result = open_url(url)
        json_ld = json.loads(result.getvalue())['data']
        graph = rdflib.Graph()
        graph.parse(data=json.dumps(json_ld), format='json-ld')
        shacl_graph.parse(data=graph.serialize(format='nt'))
    return shacl_graph

async def build_incoming_graph(file_input, rdf_urls: str) -> rdflib.Graph:
    """Builds RDF from either uploaded files or RDF urls"""
    incoming_graph = rdflib.Graph()
    _bind_namespaces(incoming_graph)
    if file_input.element.files.length > 0:
        rdf_file_names = file_input.value
        rdf_file = file_input.element.files.item(0)
        rdf_file_text = await rdf_file.text()
        rdf_type = rdflib.util.guess_format(file_input.value)
        incoming_graph.parse(data=rdf_file_text, format=rdf_type)
        file_input.clear()
    elif len(rdf_urls.value) > 0:
        rdf_file_names = rdf_urls.value
        _build_from_urls(rdf_urls.value, incoming_graph)
        rdf_urls.clear()
    
    return incoming_graph, rdf_file_names

