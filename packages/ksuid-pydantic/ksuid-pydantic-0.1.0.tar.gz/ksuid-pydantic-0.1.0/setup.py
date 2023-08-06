# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ksuid_pydantic']

package_data = \
{'': ['*']}

install_requires = \
['cyksuid>=1.1.0,<2.0.0', 'pydantic>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'ksuid-pydantic',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Justin Rubek',
    'author_email': 'rubejus@bvu.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
