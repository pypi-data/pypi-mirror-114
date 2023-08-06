# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nmappalyzer']

package_data = \
{'': ['*']}

install_requires = \
['lxml>=4.6.3,<5.0.0', 'xmltodict>=0.12.0,<0.13.0']

setup_kwargs = {
    'name': 'nmappalyzer',
    'version': '1.0.0',
    'description': "Lighweight Nmap wrapper that doesn't try too hard",
    'long_description': None,
    'author': 'TheTechromancer',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
