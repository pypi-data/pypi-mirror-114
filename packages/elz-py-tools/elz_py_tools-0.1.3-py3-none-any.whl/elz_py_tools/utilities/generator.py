import json
import os
from pathlib import Path
from ..datastore.model import DATATYPE_MAPPER, KEY_DATATYPE, KEY_RELATED_TYPE, KEY_NESTED, KEY_PLURAL


MODELS_SUBDIR = "models"


def to_snake_case(str):
    return ''.join(['_'+i.lower() if i.isupper() else i for i in str]).lstrip('_')


def generate_model(model_name, model_spec, output_dir, filename):
    """ Generate Python class for model in parameter
        Output file is generated into output_dir and model subdirectory
    """
    props_declarations = []
    links_declarations = []

    # Generate props
    for prop_name, prop_spec in model_spec.get('props', []).items():
        if prop_name == "type":  # reserved word in Python
            prop_name = prop_name + "_"

        target_type = DATATYPE_MAPPER.get(prop_spec[KEY_DATATYPE], None)
        docstring = "Return an array of values of type ".format(related_type=target_type if target_type else "object") \
            if prop_spec.get(KEY_PLURAL, False) \
            else "Return a value of type {related_type}".format(related_type=target_type if target_type else "object")

        props_declarations.append("""
    @property
    def {prop_accessor}(self):
        \"\"\" {docstring} \"\"\"
        return self.get_prop(\"{prop_name}\")
""".format(prop_accessor=to_snake_case(prop_name), docstring=docstring, prop_name=prop_name))

    # Generate links
    for link_name, link_spec in model_spec.get('links', []).items():
        internal_prop_name = link_spec.get('internalProp', None) or link_name
        related_type = link_spec['relatedType']
        docstring = "Return multiple objects of type {related_type}".format(related_type=related_type) \
            if link_spec["plural"] \
            else "Return single object of type {related_type}".format(related_type=related_type)

        links_declarations.append("""
    async def {link_accessor}(self):
        \"\"\" {docstring} \"\"\"
        return await self.get_link(\"{internal_name}\")
""".format(link_accessor=to_snake_case(link_name), docstring=docstring, internal_name=internal_prop_name))

    file_content = """from elz_py_tools.datastore.model import Model


class {class_name}(Model):

    @staticmethod
    def get_schema_type():
        return "{schema_type}"
{props}{links}""".format(
        class_name=model_spec['name'],
        schema_type=model_spec['name'],
        props=''.join(props_declarations),
        links=''.join(links_declarations))

    filepath = "{dir}/{filename}.py".format(dir=output_dir, filename=filename)
    model_file = open(filepath, "w+")
    model_file.write(file_content)
    model_file.close()


def generate_models(json_file: str, output_dir: str):
    """ Generate models contained in json schema file in argument
        Files are generated into output_dir
    """
    if not os.path.exists(json_file):
        raise Exception("json_file path does not exist")

    with open(json_file, 'r+') as f:
        model_schemas = json.load(f)

    output_path = Path(output_dir)
    if not output_path.is_dir():
        raise Exception("output_dir must be a directory or is not existing")

    # Create model subdirectory
    models_dir_path = os.path.join(output_dir, MODELS_SUBDIR)
    if not Path(models_dir_path).is_dir():
        os.mkdir(models_dir_path)

    models_built = []

    # Generate model and build tuples: (filename, classname)
    for model_name, spec in model_schemas.items():
        filename = to_snake_case(model_name)
        if filename == "yield":  # reserved word in Python
            filename = filename + "_model"

        generate_model(model_name, spec, models_dir_path, filename)
        models_built.append((filename, spec['name']))

    # Generate imports of all model classes into an __init__.py
    model_imports = "{imports}".format(imports="\n".join([
        "from .{model_dir}.{filename} import {class_name}".format(
            model_dir=MODELS_SUBDIR,
            filename=to_snake_case(model_filename),
            class_name=class_name)
        for model_filename, class_name in models_built]))

    # Generate mapping of all model classes with model name
    model_mapping = """
model_class_mapper = {{
    {mapping}
}}""".format(mapping=',\n    '.join([
        '"{class_name}": {class_name}'.format(class_name=class_name)
        for _, class_name in models_built]))

    # Generate __init__.py file
    init_file_content = """{imports}

{mapping}
""".format(imports=model_imports, mapping=model_mapping)

    init_filepath = os.path.join(output_dir, "__init__.py")
    model_file = open(init_filepath, "w+")
    model_file.write(init_file_content)
    model_file.close()


if __name__ == "__main__":
    generate_models("../datastore/test.json", "./test")
