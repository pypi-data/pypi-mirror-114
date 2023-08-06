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
    'version': '0.1.5',
    'description': 'update pijul from git.',
    'long_description': "git-pijul\n=========\n\nupdate pijul from git.\n\ninstall\n-------\n\n```bash\npip install git-pijul\n```\n\nusage\n-----\n\n```text\nUsage: git-pijul [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --help  Show this message and exit.\n  \n  Commands:\n    create  create a new pijul repository\n    update  update a repository create with git-pijul\n```\n\n`git-pijul create` finds an ancestry-path with `git rev-list --ancestry-path\n--no-merges --topo-order`. It will then checkout each revision into a temp\ndirectory and add it to pijul. Non-linear history is dropped. The last\nrevision/patchset will be forked into a channel.\n\n`git-pijul update` finds in git the shortest path from the current git-revision\nto a existing channel and updates pijul from that channel.\n\nexample\n-------\n\n```console\n$> git clone https://github.com/ganwell/git-pijul\nCloning into 'git-pijul'...\nremote: Enumerating objects: 49, done.\nremote: Counting objects: 100% (49/49), done.\nremote: Compressing objects: 100% (22/22), done.\nremote: Total 49 (delta 24), reused 49 (delta 24), pack-reused 0\nReceiving objects: 100% (49/49), 44.34 KiB | 1.93 MiB/s, done.\nResolving deltas: 100% (24/24), done.\n\n$> cd git-pijul\n\n$> git pijul create\nUsing head: 3fe9285acbb319959d9bea85abf1f10ae38e4a05 (master)\nUsing base: b215e32b5d60eb19a0676a2b9072ac7a352e1c50 ('--root')\n100%|███████████████████████████████████████████████| 10/10 [00:01<00:00,  9.75it/s]\n\n$> pijul channel\n* 3fe9285acbb319959d9bea85abf1f10ae38e4a05\n  main\n\n$> git pull\nUpdating 3fe9285..114b52f\nFast-forward\n README.md    |  4 ++++\n git_pijul.py | 58 ++++++++++++++++++++++++++++++++++------------------------\n 2 files changed, 38 insertions(+), 24 deletions(-)\n create mode 100644 README.md\n \n$> git pijul update\nUsing head: 114b52f953f397b1d025eced6ce6646a5a6c4662 (master)\nUsing base from previous update: 3fe9285acbb319959d9bea85abf1f10ae38e4a05\n100%|███████████████████████████████████████████████| 1/1 [00:00<00:00,  4.12it/s]\n\n$> pijul channel\n* 114b52f953f397b1d025eced6ce6646a5a6c4662\n  3fe9285acbb319959d9bea85abf1f10ae38e4a05\n  main\n\n```\n",
    'author': 'Jean-Louis Fuchs',
    'author_email': 'jean-louis.fuchs@adfinis-sygroup.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ganwell/git-pijul',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
