# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['metaphor']

package_data = \
{'': ['*'], 'metaphor': ['common/metadata_change_event.json']}

setup_kwargs = {
    'name': 'metaphor-models',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Metaphor',
    'author_email': 'dev@metaphor.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
