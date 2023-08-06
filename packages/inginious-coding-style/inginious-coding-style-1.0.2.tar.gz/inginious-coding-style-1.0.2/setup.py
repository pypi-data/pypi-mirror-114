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
    'version': '1.0.2',
    'description': '',
    'long_description': '# INGInious Coding Style\n\nINGInious Coding Style is a plugin for INGInious that allows tutors to grade several aspect of student submissions\' coding style.\n\nINGInious Coding Style should be easy to use for both tutors and students. The plugin adds new buttons and elements to various existing menus in the application that can be used to add and view coding style grades.\n\n## Documentation\n\nFull documentation can be found here: https://pederha.github.io/inginious-coding-style/\n\n\n## Installation\n\n```bash\npip install inginious-coding-style\n```\n\n## Configuration\n\nINGInious Coding Style is highly configurable and provides granular control over which grading categories are enabled, as well as the names and descriptions of the categories.\n\nFurthermore, experimental and cutting-edge features are made available in the `experimental` section. It is not advised to enable these settings in production. When these features are production-ready, they are moved out of the `experimental` section\n\n### Minimal Configuration\n\nThe following YAML snippet provides the default plugin configuration, and is a good starting point for exploring the plugin\'s functionality:\n\n```yml\nplugins: \n-   plugin_module: inginious_coding_style\n    name: "INGInious Coding Style"\n```\n\n### Full Configuration\n\nBelow is an example of a configuration making use of all available configuration options.\n\n```yml\nplugins: \n-   plugin_module: inginious_coding_style\n    name: "INGInious Coding Style"\n    enabled:\n        # This enables all default categories + 1 custom category\n        - comments\n        - modularity\n        - structure\n        - idiomaticity\n        - coolness # Our custom category\n    categories:\n        # This is a definition for a new category\n      - id: coolness\n        name: Coolness\n        description: How cool the code looks B-)\n      # This redefines a default category\n      - id: comments\n        name: Kommentering\n        description: Hvor godt kommentert koden er.\n    experimental:\n      merge_grades: false\n```\n\n<!-- ## Known Issues -->\n\n## TODO\n\n- [ ] Add clickable link to coding style grades for each task in task list.\n<!-- - [x] Complete -->\n<!-- - [ ] Incomplete -->\n\n## Developer Notes\n\nThis plugin uses [htmx](https://htmx.org/) to provide some interactivity.\n',
    'author': 'Peder Hovdan Andresen',
    'author_email': 'pedeha@stud.ntnu.no',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/PederHA/inginious-coding-style',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
