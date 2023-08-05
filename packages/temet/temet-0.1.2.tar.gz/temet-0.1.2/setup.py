# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['temet', 'temet.utils']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.0.1,<4.0.0',
 'aiofiles>=0.7.0,<0.8.0',
 'requests>=2.26.0,<3.0.0',
 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['temet = temet.main:app']}

setup_kwargs = {
    'name': 'temet',
    'version': '0.1.2',
    'description': '',
    'long_description': '# Temet CLI\n\nThe awesome Temet',
    'author': 'cgmark101',
    'author_email': 'cgmark101@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
