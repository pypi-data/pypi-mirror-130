# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['universal_automl']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'universal-automl',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'ixanthos',
    'author_email': 'jordan.xanthopoulos@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0.0',
}


setup(**setup_kwargs)
