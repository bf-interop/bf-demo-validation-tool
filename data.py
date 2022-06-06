import rdflib

shacl_urls = ['https://api.development.sinopia.io/resource/18b6edba-b829-47f8-9fab-05b00314bc2e',
              'https://api.development.sinopia.io/resource/c3067afb-d255-487c-834b-d40ce0ac075d',
              'https://api.development.sinopia.io/resource/ecea41b3-ce74-4e2f-8a97-299caa46fd74']

shacl_graph = rdflib.Graph()
shacl_graph.namespace_manager.bind("bf", "http://id.loc.gov/ontologies/bibframe/")
shacl_graph.namespace_manager.bind("bflc", "http://id.loc.gov/ontologies/bflc/")
shacl_graph.namespace_manager.bind("sinopia", "http://sinopia.io/vocabulary/")

