# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['autodev', 'autodev.adapters', 'autodev.entrypoints']

package_data = \
{'': ['*']}

install_requires = \
['PyGithub>=1.55,<2.0', 'click>=8.0.3,<9.0.0', 'repository_orm>=0,<1']

setup_kwargs = {
    'name': 'autodev',
    'version': '0.0.1',
    'description': 'Command line tool to automate development operations',
    'long_description': None,
    'author': 'Lyz',
    'author_email': 'lyz@riseup.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<=3.10',
}


setup(**setup_kwargs)
