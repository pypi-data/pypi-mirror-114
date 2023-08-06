# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src', 'src.mytypes', 'src.search']

package_data = \
{'': ['*']}

install_requires = \
['pyprof2calltree>=1.4.5,<2.0.0']

setup_kwargs = {
    'name': 'jumper-py',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'David',
    'author_email': 'davigetto@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
