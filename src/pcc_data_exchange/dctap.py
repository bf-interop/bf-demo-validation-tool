"""Initial support for DCTAP <https://github.com/dcmi/dctap> to BF SHACL validation"""
__author__ = "Jeremy Nelson"
import io

import pandas as pd
import rdflib

BF = rdflib.Namespace("http://id.loc.gov/ontologies/bibframe/")
BFLC = rdflib.Namespace("http://id.loc.gov/ontologies/bflc/")
SHACL = rdflib.Namespace("http://www.w3.org/ns/shacl#")
SINOPIA = rdflib.Namespace("http://sinopia.io/vocabulary/")


def _sh_datatype(datatype: str,
                 property_bnode: rdflib.BNode,
                 graph: rdflib.Graph):
    """Adds a SHACL datatype to a property shape"""
    match datatype:
        case "rdf:langString":
            graph.add((property_bnode, SHACL.datatype, rdflib.RDF.langString))

        case "xsd:string":
            graph.add((property_bnode, SHACL.datatype, rdflib.XSD.string))


def _add_property(row: dict, graph: rdflib.Graph):
    """Adds a SHACL Node Property to the shape graph"""
    shape_id = rdflib.URIRef(row['shapeID'])
    node_shape = graph.value(subject=shape_id, predicate=rdflib.RDF.type)
    # SHACL Node Shape not in graph, adds shape_id as a SHACL graph
    if node_shape is None:
        graph.add((shape_id, rdflib.RDF.type, SHACL.NodeShape))
        graph.add((shape_id, rdflib.RDFS.label, rdflib.Literal(row['shapeLabel'])))

    # Adds SHACL Property Shape
    property_bnode = rdflib.BNode()
    graph.add((shape_id, SHACL.property, property_bnode))
    graph.add((property_bnode, rdflib.RDF.type, SHACL.PropertyShape))
    graph.add((property_bnode, SHACL.path, rdflib.URIRef(row['propertyID'])))
    if row['mandatory'] is True:
        graph.add((property_bnode, SHACL.minCount, rdflib.Literal(1)))
    if row["repeatable"] is False:
        graph.add((property_bnode, SHACL.maxCount, rdflib.Literal(1)))
    _sh_datatype(row["valueDataType"], property_bnode, graph)
        


    

async def handler(file_input, dctap_element, shacl_graph: rdflib.Graph) -> rdflib.Graph:
    """Loads CSV of DC Tabular Application Profile and adds to validation 
    loaded SHACL graph"""
    if file_input.element.files.length > 0:
        dctap_file = file_input.element.files.item(0)
        dctap_text = await dctap_file.text()
        dctap_df = pd.read_csv(io.StringIO(dctap_text))
        for row in dctap_df.iterrows():
            _add_property(row[1], shacl_graph)
    dctap_element.clear()
    dctap_element.element.innerHTML = dctap_df.to_html(index=False)
    return shacl_graph

