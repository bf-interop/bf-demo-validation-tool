import unittest

import rdflib

import validation

class ValidationUnitTests(unittest.TestCase):

   def test_serialize_graph(self):
        graph = rdflib.Graph()
        graph.add(
          (rdflib.URIRef("https://example.org/big"), 
           rdflib.RDF.type,
           rdflib.URIRef("https://bibframe.org/Work"))
        )
        pre = validation._serialize_graph(
            graph=graph,
            container=None,
        )
        assert "https://example.org/big" in str(pre.innerHTML)
