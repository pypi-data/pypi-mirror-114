# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['git_pijul']
install_requires = \
['click>=8.0.1,<9.0.0', 'temppathlib>=1.1.0,<2.0.0', 'tqdm>=4.61.2,<5.0.0']

entry_points = \
{'console_scripts': ['git-pijul = git_pijul:main']}

setup_kwargs = {
    'name': 'git-pijul',
    'version': '0.1.0',
    'description': 'update pijul from git.',
    'long_description': None,
    'author': 'Jean-Louis Fuchs',
    'author_email': 'jean-louis.fuchs@adfinis-sygroup.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
