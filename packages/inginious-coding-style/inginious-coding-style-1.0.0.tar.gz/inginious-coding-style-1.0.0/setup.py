# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['inginious_coding_style']

package_data = \
{'': ['*'], 'inginious_coding_style': ['templates/*']}

install_requires = \
['inginious>=0.7,<0.8', 'pydantic>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'inginious-coding-style',
    'version': '1.0.0',
    'description': '',
    'long_description': None,
    'author': 'Peder Hovdan Andresen',
    'author_email': 'pedeha@stud.ntnu.no',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
