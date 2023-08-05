
DATATYPE_MAPPER = {
    # Rdf types
    'rdfs:Literal': str,
    'http://www.w3.org/2000/01/rdf-schema#Literal': str,
    'http://www.w3.org/2001/XMLSchema#Literal': str,
    'http://www.w3.org/2001/XMLSchema#string': str,
    'http://www.w3.org/2001/XMLSchema#anyURI': str,
    'http://www.w3.org/2001/XMLSchema#short': int,
    'http://www.w3.org/2001/XMLSchema#int': int,
    'http://www.w3.org/2001/XMLSchema#integer': int,
    'http://www.w3.org/2001/XMLSchema#float': float,
    'http://www.w3.org/2001/XMLSchema#boolean': bool,
    'http://www.w3.org/2001/XMLSchema#date': str,
    'http://www.w3.org/2001/XMLSchema#dateTime': str,
    'http://www.w3.org/2001/XMLSchema#dateTimeStamp': str,
    'http://www.w3.org/2001/XMLSchema#duration': str,
    'http://www.w3.org/2001/XMLSchema#gMonth': str,
    'http://www.opengis.net/ont/geosparql#wktLiteral': str,
    'http://www.opengis.net/ont/geosparql#gmlLiteral': str,
    'http://www.elzeard.co/ontologies/c3po/time#rdate': str,
    # Mongo types
    "Int": int,
    "Float": float,
    'String': str,
    'Boolean': bool
}

KEY_NAME = 'name'
KEY_RDF_TYPE = 'rdfType'
KEY_INDEX_TYPE = 'indexType'
KEY_MONGO_TYPE = 'mongoType'
KEY_DATATYPE = 'dataType'
KEY_INTERNAL_PROP = 'internalProp'
KEY_RELATED_TYPE = 'relatedType'
KEY_NESTED = 'nested'
KEY_PLURAL = 'plural'
