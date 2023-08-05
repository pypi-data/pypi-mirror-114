

# TODO: consider using and extending SPARQLBurger (https://pmitzias.com/SPARQLBurger/) ?


class SPARQLBuilder(object):
    """ Wrapper for building some SPARQL queries """

    def __init__(self, prefixes_mapping: dict, nodes_namespace_uri: str, nodes_prefix: str):
        self._prefixes_mapping = prefixes_mapping
        self._nodes_prefix = nodes_prefix
        self._nodes_namespace_uri = nodes_namespace_uri

    def build_construct_object_query(self, node_type: str, object_uri: str):
        """ Build a construct query for getting properties of uri in parameter """ 
        if ':' not in node_type:
            raise Exception('Node type must contain prefix')
        type_prefix, type_suffix = node_type.split(':')
        node_type_uri = f'{self._prefixes_mapping[type_prefix]}{type_suffix}'

        return f'''
{self._build_prefixes()}
CONSTRUCT {{
    <{object_uri}> ?p ?o .
    <{object_uri}> a <{node_type_uri}>
}} where {{
    <{object_uri}> ?p ?o .
    <{object_uri}> a <{node_type_uri}>
}}
'''

    def build_construct_objects_query(self, node_type: str):
        """ Build a construct query for getting nodes and properties of uris of type in parameter """
        if ':' not in node_type:
            raise Exception('Node type must contain prefix')
        type_prefix, type_suffix = node_type.split(':')
        node_type_uri = f'{self._prefixes_mapping[type_prefix]}{type_suffix}'

        return f'''
{self._build_prefixes()}
CONSTRUCT {{
    ?s ?p ?o .
    ?s a <{node_type_uri}>
}} where {{
    ?s ?p ?o .
    ?s a <{node_type_uri}>
}}
    '''

    def _build_prefixes(self):
        """ Build PREFIX part of query """
        return '\n'.join(f'PREFIX {prefix}: <{uri}>' for prefix, uri in self._prefixes_mapping.items())
