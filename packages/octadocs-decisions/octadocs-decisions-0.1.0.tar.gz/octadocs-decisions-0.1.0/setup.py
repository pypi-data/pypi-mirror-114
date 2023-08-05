# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['octadocs_decisions']

package_data = \
{'': ['*'], 'octadocs_decisions': ['templates/octadocs-decisions/*', 'yaml/*']}

entry_points = \
{'mkdocs.plugins': ['octadocs_decisions = '
                    'octadocs_decisions.plugin:DecisionsPlugin']}

setup_kwargs = {
    'name': 'octadocs-decisions',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Anatoly Scherbakov',
    'author_email': 'altaisoft@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
