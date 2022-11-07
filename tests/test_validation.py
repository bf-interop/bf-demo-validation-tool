import unittest

import rdflib

import validation

class ValidationUnitTests(unittest.TestCase):

   def test_serialize_graph(self):
        graph = rdflib.Graph()
        graph.add(
          (rdflib.URIRef("http://sinopia.io/id"), 
           rdflib.RDF.type,
           rdflib.URIRef("http://bibframe.org/Work"))
        )
        pre = validation._serialize_graph(
            graph=graph,
            container=None,
        )
        assert "http://sinopia.io/id" in str(pre.innerHTML)
