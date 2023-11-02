"""Initial support for DCTAP <https://github.com/dcmi/dctap> to BF SHACL validation"""
__author__ = "Jeremy Nelson"
import io
import sys

import numpy as np
import pandas as pd
import rdflib

BF = rdflib.Namespace("http://id.loc.gov/ontologies/bibframe/")
BFLC = rdflib.Namespace("http://id.loc.gov/ontologies/bflc/")
SHACL = rdflib.Namespace("http://www.w3.org/ns/shacl#")
SINOPIA = rdflib.Namespace("http://sinopia.io/vocabulary/")


def _sh_datatype(datatype: str, property_bnode: rdflib.BNode, graph: rdflib.Graph):
    """Adds a SHACL datatype to a property shape"""
    match datatype:
        case "rdf:langString":
            graph.add((property_bnode, SHACL.datatype, rdflib.RDF.langString))

        case "xsd:string":
            graph.add((property_bnode, SHACL.datatype, rdflib.XSD.string))


def _sh_value_constraint(
    value_constraint: str,
    value_constraint_type: str,
    property_bnode: rdflib.BNode,
    graph: rdflib.Graph,
):
    """Adds a value constraint type to a property shape"""
    match value_constraint_type:
        case "picklist":
            pass

        case "IRIstem":
            pass

        case "pattern":
            graph.add((property_bnode, SHACL.pattern, rdflib.Literal(value_constraint)))

        case "languageTag":
            pass

        case "minLength":
            graph.add(
                (property_bnode, SHACL.minLength, rdflib.Literal(value_constraint))
            )

        case "maxLength":
            graph.add(
                (property_bnode, SHACL.maxLength, rdflib.Literal(value_constraint))
            )

        case "minInclusive":
            graph.add(
                (property_bnode, SHACL.minInclusive, rdflib.Literal(value_constraint))
            )

        case "maxInclusive":
            graph.add(
                (property_bnode, SHACL.maxInclusive, rdflib.Literal(value_constraint))
            )


def _add_property(row: dict, graph: rdflib.Graph):
    """Adds a SHACL Node Property to the shape graph"""
    shape_id = rdflib.URIRef(row["shapeID"])
    node_shape = graph.value(subject=shape_id, predicate=rdflib.RDF.type)
    # SHACL Node Shape not in graph, adds shape_id as a SHACL graph
    if node_shape is None:
        graph.add((shape_id, rdflib.RDF.type, SHACL.NodeShape))
        graph.add((shape_id, rdflib.RDFS.label, rdflib.Literal(row["shapeLabel"])))
    # Adds SHACL Property Shape
    property_bnode = rdflib.BNode()
    graph.add((shape_id, SHACL.property, property_bnode))
    graph.add((property_bnode, rdflib.RDF.type, SHACL.PropertyShape))
    graph.add((property_bnode, rdflib.RDFS.label, rdflib.Literal(row["propertyLabel"])))
    if row["propertyID"].startswith("bf:"):
        path_object = getattr(BF, row["propertyID"].split(":")[-1])
    else:
        path_object = rdflib.URIRef(row["propertyID"])
    graph.add((property_bnode, SHACL.path, path_object))
    if "severity" in row:
        match row["severity"]:
            case "Violation":
                severity_level = SHACL.Violation

            case "Warning":
                severity_level = SHACL.Warning

            case _:
                severity_level = SHACL.Info

        graph.add((property_bnode, SHACL.severity, severity_level))
    if row["mandatory"] is True:
        graph.add((property_bnode, SHACL.minCount, rdflib.Literal(1)))
    if row["repeatable"] is False:
        graph.add((property_bnode, SHACL.maxCount, rdflib.Literal(1)))
    if "valueDataType" in row:
        _sh_datatype(row["valueDataType"], property_bnode, graph)


async def handler(file_input, dctap_element, shacl_graph: rdflib.Graph) -> rdflib.Graph:
    """Loads CSV of DC Tabular Application Profile and adds to validation
    loaded SHACL graph"""
    if file_input.element.files.length > 0:
        dctap_file = file_input.element.files.item(0)
        dctap_text = await dctap_file.text()
        try:
            dctap_df = pd.read_csv(io.StringIO(dctap_text))
            dctap_df = dctap_df.replace({np.nan: None})
        except Exception as e:
            print(sys.exc_info())
        for i, row in enumerate(dctap_df.iterrows()):
            if row[1]["shapeID"] is None:
                continue
            try:
                _add_property(row[1], shacl_graph)
            except Exception as e:
                print(sys.exc_info())
    dctap_element.clear()
    raw_shacl = shacl_graph.serialize(format="turtle")
    raw_shacl = raw_shacl.replace("<", "&lt;").replace(">", "&gt;")
    dctap_element.element.innerHTML = (
        f"""<h3>Resulting SHACL</h3><pre>{raw_shacl}</pre>"""
    )
    # """<div>{dctap_df.to_html(index=False)}</div>"""<pre>{}</pre>"""
    return shacl_graph
