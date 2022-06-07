import rdflib

import js
from data import SHACL

def validation_html(validation_result, failure_text: str, graph: rdflib.Graph) -> str:
    validation_result.clear()
    pre = js.document.createElement("pre")
    pre.innerHTML = failure_text.replace("<", "&lt;").replace(">", "&gt;")
    validation_result.element.appendChild(pre)