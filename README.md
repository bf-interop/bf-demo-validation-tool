# BIBFRAME Interoperability Validation Tool 

This web application, live at [https://bf-interop.github.io/bf-demo-validation-tool/](https://bf-interop.github.io/bf-demo-validation-tool/),
is a demonstration of validating BIBFRAME RDF resources using
[DCTAP](https://github.com/dcmi/dctap) tab-separated files that is converted into one or more 
[SHACL](https://www.w3.org/TR/shacl/) graphs. 

The web application uses [pyscript](https://pyscript.net/)
and the [rdflib](https://github.com/RDFLib/rdflib), [pyshacl](https://github.com/RDFLib/pySHACL), and 
[pandas](https://pandas.pydata.org/) to load and then validate incoming BIBFRAME RDF using
either the upload button or by entering a direct URL of the BIBFRAME resource.

**NOTE:** We expect BIBFRAME vendors to have their own validation technology stack that could use the 
SHACL produced this tool but the intention of the BIBFRAME Interoperability Validation Tool is **NOT** to be a
production-level service.

# Contributing
Contributions are very welcome. To learn more, see the [Contributor Guide](CONTRIBUTING.md).

# License

Distributed under the terms of the [Apache 2.0
license](https://opensource.org/licenses/Apache-2.0), the *BIBFRAME Interoperability Validation Tool* 
is free and open source software.

# Issues
If you encounter any problems, please [file an issue](https://github.com/bf-interop/bf-demo-validation-tool/issues) 
along with a detailed description.

