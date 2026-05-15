"""Initial support for DCTAP <https://github.com/dcmi/dctap> to BF SHACL validation"""

__author__ = "Jeremy Nelson"
import os
import js
import sys

import rdflib

from dctap2shacl import  DCTap2SHACLTransformer, BF


async def handler(file_input, dctap_element, shacl_graph: rdflib.Graph) -> rdflib.Graph:
    """Loads CSV of DC Tabular Application Profile and adds to validation
    loaded SHACL graph"""
    dctap_error = js.document.getElementById("dctap-error")
    dctap_error_body = js.document.getElementById("dctap-error-body")

    if file_input.files.length > 0:
        try:
            dctap_file = file_input.files.item(0)
            dctap_text = await dctap_file.text()
            tmp_path = "/tmp/dctap_input.tsv"
            with open(tmp_path, "w") as tmp:
                tmp.write(dctap_text)
            transformer = DCTap2SHACLTransformer()
            transformer.run(tmp_path)
            os.unlink(tmp_path)
            shacl_graph = transformer.graph
        except Exception as e:
            dctap_error.classList.remove("d-none")
            dctap_error_body.innerHTML = sys.exc_info()
            return
    raw_shacl = shacl_graph.serialize(format="turtle")
    raw_shacl = raw_shacl.replace("<", "&lt;").replace(">", "&gt;")
    dctap_element.innerHTML = f"""<h3>Resulting SHACL</h3><pre>{raw_shacl}</pre>"""
    return shacl_graph
