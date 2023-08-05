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
    'version': '0.2.1',
    'description': 'This is my package that tests out Typer.',
    'long_description': '# `odc-typer-test`\n\nAwesome CLI user manager. Based on [this tutorial](https://typer.tiangolo.com/tutorial/).\n\n**Usage**:\n\n```console\n$ odc-typer-test [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n* `--install-completion`: Install completion for the current shell.\n* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n* `--help`: Show this message and exit.\n\n**Commands**:\n\n* `create`: Create a new user with USERNAME.\n* `delete`: Delete an existing user with USERNAME.\n* `delete-all`: Delete all users in the database.\n* `init`: Initialize the user database.\n\n## `odc-typer-test create`\n\nCreate a new user with USERNAME.\n\n**Usage**:\n\n```console\n$ odc-typer-test create [OPTIONS] USERNAME\n```\n\n**Arguments**:\n\n* `USERNAME`: The name of user to create.  [required]\n\n**Options**:\n\n* `--help`: Show this message and exit.\n\n## `odc-typer-test delete`\n\nDelete an existing user with USERNAME.\n\nIf --force is not used, confirmation is required.\n\n**Usage**:\n\n```console\n$ odc-typer-test delete [OPTIONS] USERNAME\n```\n\n**Arguments**:\n\n* `USERNAME`: The name of user to delete.  [required]\n\n**Options**:\n\n* `--force / --no-force`: Force deletion without confirmation.  [required]\n* `--help`: Show this message and exit.\n\n## `odc-typer-test delete-all`\n\nDelete all users in the database.\n\nIf --force is not used, confirmation is required.\n\n**Usage**:\n\n```console\n$ odc-typer-test delete-all [OPTIONS]\n```\n\n**Options**:\n\n* `--force / --no-force`: Force deletion without confirmation.  [required]\n* `--help`: Show this message and exit.\n\n## `odc-typer-test init`\n\nInitialize the user database.\n\n**Usage**:\n\n```console\n$ odc-typer-test init [OPTIONS]\n```\n\n**Options**:\n\n* `--help`: Show this message and exit.\n',
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
