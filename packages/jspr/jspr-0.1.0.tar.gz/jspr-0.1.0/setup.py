# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jspr']

package_data = \
{'': ['*']}

install_requires = \
['typing-extensions>=4.0.1,<5.0.0']

entry_points = \
{'console_scripts': ['jspr = jspr.main:start']}

setup_kwargs = {
    'name': 'jspr',
    'version': '0.1.0',
    'description': 'A JSON Processor',
    'long_description': None,
    'author': 'vector-of-bool',
    'author_email': 'vectorofbool@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
