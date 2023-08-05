# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['odc_typer_test']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['odc-typer-test = odc_typer_test.main:app']}

setup_kwargs = {
    'name': 'odc-typer-test',
    'version': '0.1.0',
    'description': 'This is my package that tests out Typer.',
    'long_description': "# Typer Test\n\nI'm testing [Typer](/typer.tiangolo.com) here. What do you think?\n",
    'author': 'one-data-cookie',
    'author_email': 'kolacek.m@gmail.com',
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
