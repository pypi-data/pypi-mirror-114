# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['elz_py_tools',
 'elz_py_tools.datastore',
 'elz_py_tools.drivers',
 'elz_py_tools.drivers.amqp',
 'elz_py_tools.drivers.graph',
 'elz_py_tools.drivers.index',
 'elz_py_tools.drivers.mongo',
 'elz_py_tools.drivers.toolkit',
 'elz_py_tools.tasks',
 'elz_py_tools.utilities']

package_data = \
{'': ['*']}

install_requires = \
['aio-pika>=6.8.0,<7.0.0',
 'elasticsearch>=7.13.3,<8.0.0',
 'pymongo>=3.11.4,<4.0.0']

setup_kwargs = {
    'name': 'elz-py-tools',
    'version': '0.1.3',
    'description': 'Python components compliant with Synaptix framework',
    'long_description': '# Python tools\n\nRequires Python 3.8+\n\nPyPI : https://pypi.org/project/elz-py-tools/\n\nThis repository contains some Python components used in Elzeard project.\nThese components contain AMQP client and drivers for connecting databases. They are made to be working along with synaptix framework created by Mnemotix (https://gitlab.com/mnemotix).\n\nThis repository uses Poetry for package dependencies (https://python-poetry.org/).\n\nFor working on these components or new ones, install poetry and install package dependencies by running :\n\n> poetry install\n\nFor using it locally from another repository :\n\n> poetry build\n\n> pip install <local_path_to_this_repo>\n\n\n## Datastore and drivers\n\nTODO: to complete...\n\n\n## Model generator\n\nModel files can be generated for facilitating use of this framework and querying of graph and index\nTODO: complete doc...\n\nHere is the format of the schema json file, which is used by datastore :\n```\n[{\n    schema1: {\n        props: {\n            <prop1>: { dataType: <string> }\n        },\n        links: {\n            <link1>: { relatedType: <string>, nested: <boolean>, plural: <boolean> }\n        }\n    },\n    ...\n}]\n```\n\n## TODO:\n\n- Implements GraphDriver.get_nodes method\n- Add possibility to query a label property in a specific language\n- Option for passing custom datatype mapping in datastore',
    'author': 'Hervé',
    'author_email': 'herve.descombe@elzeard.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/elzeard/elz-py-tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
