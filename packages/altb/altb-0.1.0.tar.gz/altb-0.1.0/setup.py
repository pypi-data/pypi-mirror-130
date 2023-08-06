# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['altb']

package_data = \
{'': ['*']}

install_requires = \
['blessed>=1.19.0,<2.0.0',
 'getch>=1.0,<2.0',
 'pydantic>=1.8.2,<2.0.0',
 'rich>=10.15.2,<11.0.0',
 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['altb = altb.main:main']}

setup_kwargs = {
    'name': 'altb',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Elran Shefer',
    'author_email': 'elran777@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
