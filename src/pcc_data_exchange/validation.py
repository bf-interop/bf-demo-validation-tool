import json

import js
import pyshacl
import rdflib

from pyodide.http import open_url

from data import SHACL

def summarize(*args, **kwargs):
    shacl_summary = kwargs.get("summary_element")
    current_shacl = kwargs.get("graph")
    shapes = {}

    shacl_summary.clear()

    for row in current_shacl.query("""PREFIX sh: <http://www.w3.org/ns/shacl#>
    SELECT ?node_shape ?label ?target
    WHERE { ?node_shape a sh:NodeShape .
            ?node_shape rdfs:label ?label . 
            ?node_shape sh:targetClass ?target .}
    ORDER BY ?label """):
        key = str(row[0])
        if not key in shapes:
            shapes[key] = {
                "id": row[0],
                "label": str(row[1]),
                "targets": [row[2],],
            }
            continue
        shapes[key]["targets"].append(row[2])
    for key, shape in shapes.items():
        shape_tr = _add_shape(current_shacl, shape)
        shacl_summary.element.appendChild(shape_tr)

    # Change label
    shacl_label = js.document.getElementById("shacl_size")
    shacl_label.innerHTML = f"{len(current_shacl)} triples from {len(shapes)} Sinopia SHACL Resources"
        
 
      
def _add_property_summary(properties, tr):
    td = js.document.createElement("td")
    unordered_list = js.document.createElement("ul")
    for values in properties.values():
        for row in values:
            li = js.document.createElement("li")
            li.innerText = f"{row[0]}: {row[1]}"
            unordered_list.appendChild(li)
    td.appendChild(unordered_list)
    tr.appendChild(td)

def _add_shape(validation_graph: rdflib.Graph, shape: dict):
    shape_tr = js.document.createElement("tr")
    shape_td = js.document.createElement("td")
    anchor = js.document.createElement("a")
    anchor.setAttribute("href", shape["id"])
    anchor.innerText = shape["label"]
    shape_td.appendChild(anchor)
    shape_tr.appendChild(shape_td)
    target_td = js.document.createElement("td")
    for target_class in shape["targets"]:
        target_p = js.document.createElement("p")
        target_p.innerText = target_class
        target_td.appendChild(target_p)
    shape_tr.appendChild(target_td)
    properties = {}
    for obj in validation_graph.objects(subject=shape["id"],
                             predicate=SHACL.property):
        path = validation_graph.value(subject=obj, predicate=SHACL.path)
        path_key = str(path)
        if not path_key in properties:
            properties[path_key] = [("path", str(path))]
        min_count = validation_graph.value(subject=obj, predicate=SHACL.minCount)
        if min_count:
            properties[path_key].append(("miniumum count", int(min_count)))
        pattern = validation_graph.value(subject=obj, predicate=SHACL.pattern)
        if pattern:
            properties[path_key].append(("regular expression pattern", str(pattern)))
    _add_property_summary(properties, shape_tr)
    return shape_tr

def _result_html(parent_element, failure_text: str, graph: rdflib.Graph) -> str:
    pre = js.document.createElement("pre")
    pre.setAttribute("style", "margin: 1em;")
    pre.innerHTML = failure_text.replace("<", "&lt;").replace(">", "&gt;")
    parent_element.appendChild(pre)


def _serialize_graph(*args, **kwargs):
    graph = kwargs.get("graph")
    pre = js.document.createElement("pre")
    rdf_format = kwargs.get("format", "turtle")
    serialized_str = graph.serialize(format=rdf_format)
    serialized_str = serialized_str.replace("<", "&lt;").replace(">", "&gt;")
    pre.innerHTML = serialized_str
    return pre

async def validate(*args, **kwargs):
    incoming_graph = kwargs.get("graph")
    validation_graph = kwargs.get("shacl")
    validation_element = kwargs.get("results_element")
    rdf_file_names = kwargs.get("source_rdf")

    validation_element.clear()


    row = js.document.createElement("div")
    row.classList.add("row")

    results_col = js.document.createElement("div")
    results_col.classList.add("col")
    row.appendChild(results_col)
    serialized_col = js.document.createElement("div")
    serialized_col.classList.add("col")
    row.appendChild(serialized_col)

    if len(incoming_graph) > 0:
        conforms, results_graph, results_text = pyshacl.validate(incoming_graph, shacl_graph=validation_graph, allow_warnings=True)
        alert = js.document.createElement("div")
        alert.setAttribute("style", "margin: 1em;")
        alert.setAttribute("role", "alert")
        alert_msg = f"{rdf_file_names} with {len(incoming_graph)} triples"
        css_classes = ["alert", "alert-dismissible", "fade", "show"]
        if conforms:
            css_classes.append("alert-success")
            alert.innerText = f"{alert_msg} Passed!!"
        else:
            css_classes.append("alert-danger")
            alert.innerText = f"{alert_msg} Failed!"
        for css_class in css_classes:
            alert.classList.add(css_class)
        validation_element.element.appendChild(alert)
        _result_html(results_col, results_text, results_graph)
        incoming_title = js.document.createElement("h3")
        incoming_title.innerHTML = f"Incoming graph {rdf_file_names}"
        serialized_col.appendChild(incoming_title)
        serialized_pre = _serialize_graph(graph=incoming_graph)
        serialized_col.appendChild(serialized_pre)
    validation_element.element.appendChild(row)
