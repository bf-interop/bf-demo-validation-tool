import rdflib

shacl_urls = ['https://api.development.sinopia.io/resource/18b6edba-b829-47f8-9fab-05b00314bc2e',
              'https://api.development.sinopia.io/resource/c3067afb-d255-487c-834b-d40ce0ac075d',
              'https://api.development.sinopia.io/resource/ecea41b3-ce74-4e2f-8a97-299caa46fd74',
              'https://api.development.sinopia.io/resource/9c496dbc-8717-4a17-a8ac-46e25f0f4c71',
              'https://api.development.sinopia.io/resource/0733f929-011a-4865-8c80-ef69449f1a25',
              'https://api.development.sinopia.io/resource/137a8f9d-bee3-410d-b224-aa3712013662' ]

shacl_graph = rdflib.Graph()
shacl_graph.namespace_manager.bind("bf", "http://id.loc.gov/ontologies/bibframe/")
shacl_graph.namespace_manager.bind("bflc", "http://id.loc.gov/ontologies/bflc/")
shacl_graph.namespace_manager.bind("sinopia", "http://sinopia.io/vocabulary/")

