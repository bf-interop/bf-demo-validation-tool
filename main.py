
import asyncio
# import json
import sys
import datetime as dt
# from traceback import format_exc

import js
# from pyodide.http import open_url

import pyshacl
from rdflib import Graph, Namespace, Literal


# shacl_urls = []


import validation
import dctap
from data import SHACL, init_shacl_graph, build_incoming_graph



# shacl_graph = init_shacl_graph(shacl_urls)

today = js.document.getElementById('today')
today.innerHTML = dt.datetime.now().strftime('%A %B %d, %Y')

splash_modal_close_btn = js.document.getElementById('splashModalCloseBtn')
splash_modal_close_btn.click()

# shacl_summary = Element("shacl_summary")

# validation.summarize(summary_element=shacl_summary, graph=shacl_graph)

# rdf_url = Element("rdf-url")
# upload_control = Element("upload-rdf")
# validation_result = Element("validation-result")
incoming_graphs = []


# sh = Namespace("http://www.w3.org/ns/shacl#")

# async def validate_rdf(*args, **kwargs):
#     graph, source_rdf_names = await build_incoming_graph(upload_control, 
#                                                         rdf_url)
#     incoming_graphs.append(graph)

#     await validation.validate(graph=graph,
#                             shacl=shacl_graph,
#                             source_rdf=source_rdf_names,
#                             results_element=validation_result)


# async def run_tests(*args, **kwargs):
#     from test_validation import ValidationUnitTests
#     validation_display = Element("test-results")
#     validation_test = ValidationUnitTests()
#     try:
#         validation_test.test_serialize_graph()
#         msg = "All Tests Passed"
#     except AssertionError as err:
#         msg = format_exc()
#     validation_display.element.innerHTML = msg


async def load_dctap(*args, **kwargs):
    global shacl_graph
    use_existing_shacl_ckbox = js.document.getElementById("use-existing-shacl")
    dctap_file = js.document.getElementById("upload-dctap")
    dctap_table = js.document.getElementById("dctap-table")
    shacl_summary = js.document.getElementById("shacl_summary")

    if use_existing_shacl_ckbox.checked:
        dctap_graph = shacl_graph
    else:
        dctap_graph = init_shacl_graph([])
    shacl_graph = await dctap.handler(dctap_file, dctap_table, dctap_graph)
    validation.summarize(summary_element=shacl_summary, graph=shacl_graph)
    

