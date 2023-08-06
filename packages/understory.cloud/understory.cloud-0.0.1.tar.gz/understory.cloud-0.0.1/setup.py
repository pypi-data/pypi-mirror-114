# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['understory_cloud']

package_data = \
{'': ['*'], 'understory_cloud': ['static/*', 'templates/*']}

install_requires = \
['understory>=0.0.46,<0.0.47']

setup_kwargs = {
    'name': 'understory.cloud',
    'version': '0.0.1',
    'description': 'Navigate the various projects tangential to the understory.',
    'long_description': None,
    'author': 'Angelo Gladding',
    'author_email': 'angelo@lahacker.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
