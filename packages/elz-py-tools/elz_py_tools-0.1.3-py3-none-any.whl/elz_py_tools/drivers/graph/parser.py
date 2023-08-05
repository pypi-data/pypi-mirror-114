

def castValueForDataType(datatype: str, value):
    """ Cast rdf literal into pythonic type """
    if datatype in [
        "http://www.w3.org/2001/XMLSchema#float",
        "http://www.w3.org/2001/XMLSchema#double",
        "http://www.w3.org/2001/XMLSchema#timestamp"
    ]:
        return float(value)
    elif datatype in [
        "http://www.w3.org/2001/XMLSchema#int",
        "http://www.w3.org/2001/XMLSchema#integer"
    ]:
        return int(value)
    elif datatype in [
        "http://www.w3.org/2001/XMLSchema#boolean"
    ]:
        return value if type(value) == bool else value == "true"
    elif datatype in [
        "http://www.w3.org/2001/XMLSchema#date",
        "http://www.w3.org/2001/XMLSchema#dateTime",
        "http://www.w3.org/2001/XMLSchema#dateTimeStamp"
    ]:
        return int(value)
    else:
        return value


def parse_construct_result(bindings):
    """ Parse result of construct query to convert bindings into a set of entities with corresponding properties """
    entities = []
    for binding in bindings:
        rdf_props = filter(lambda x: x not in ['@id', '@type'], binding.keys())
        entity_props = []
        for rdf_prop in rdf_props:
            value = binding[rdf_prop]
            if '#' in rdf_prop:
                prefix, prop_name = rdf_prop.split('#')
            else:
                prefix = rdf_prop[0:rdf_prop.rfind('/')+1]
                prop_name = rdf_prop[rdf_prop.rfind('/')+1:]
            entity_props.append([prefix, prop_name, value])
        entities.append({
            '@id': binding['@id'],
            '@type': binding['@type'],
            'properties': entity_props
        })

    parsed_objects = []
    for focused_entity in entities:
        fields = {
            "id": focused_entity['@id'],
            "uri": focused_entity['@id'],
            "types": focused_entity['@type']
        }
        for prefix, prop_name, value in focused_entity['properties']:
            if '@id' in value[0]:
                fields[prop_name] = []
                for target in value:
                    nested_entity = next((obj for obj in entities if obj['@id'] == target['@id']), None)
                    fields[prop_name].append(target['@id'])
            elif '@language' in value[0]:
                fields[prop_name] = list(map(lambda label: label['@value'], value))
                fields[f'{prop_name}_locales'] = list(map(lambda label: label.get('@language', 'en'), value))
            else:
                fields[prop_name] = castValueForDataType(value[0].get('@type', None), value[0]['@value'])
        parsed_objects.append(fields)

    return parsed_objects
