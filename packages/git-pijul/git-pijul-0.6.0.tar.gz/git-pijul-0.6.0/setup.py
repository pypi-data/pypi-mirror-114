# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['git_pijul']
install_requires = \
['click>=8.0.1,<9.0.0',
 'temppathlib>=1.1.0,<2.0.0',
 'toml>=0.10.2,<0.11.0',
 'tqdm>=4.61.2,<5.0.0']

entry_points = \
{'console_scripts': ['git-pijul = git_pijul:main']}

setup_kwargs = {
    'name': 'git-pijul',
    'version': '0.6.0',
    'description': 'update pijul from git.',
    'long_description': "git-pijul\n=========\n\nupdate pijul from git.\n\ninstall\n-------\n\n```bash\npip install git-pijul\n```\n\nusage\n-----\n\n```text\nUsage: git-pijul [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  create   Create a new pijul repository and import a linear history\n  plot     Display current changes as graphviz file (git pijul plot | dot...\n  shallow  create a new pijul repository from the current revision...\n  update   Update a repository created with git-pijul\n```\n\n`git-pijul create` finds an ancestry-path with `git rev-list --ancestry-path\n--no-merges --topo-order`. It will then checkout each revision into a temp\ndirectory and add it to pijul. Non-linear history is dropped. The last\nrevision/patchset will be forked into a channel.\n\n`git-pijul update` finds in git the shortest path from the current git-revision\nto a existing channel and updates pijul from that channel.\n\n`git-pijul shallow` create a new pijul repository from the current revision without\nhistory.\n\n`git-pijul plot` plots dependencies of all changes, with `-i` you can exclude changes from a\nchannel, usually the `main` channel that contains published changes. This allows\nyou to select the changes you want to publish.\n\nexample\n-------\n\n```console\n$> git clone https://github.com/ganwell/git-pijul\nCloning into 'git-pijul'...\nremote: Enumerating objects: 49, done.\nremote: Counting objects: 100% (49/49), done.\nremote: Compressing objects: 100% (22/22), done.\nremote: Total 49 (delta 24), reused 49 (delta 24), pack-reused 0\nReceiving objects: 100% (49/49), 44.34 KiB | 1.93 MiB/s, done.\nResolving deltas: 100% (24/24), done.\n\n$> cd git-pijul\n\n$> git pijul create\nUsing head: 3bc7b1e8618681d4e3069989160998f7d366f08c (HEAD)\nUsing base: b215e32b5d60eb19a0676a2b9072ac7a352e1c50 ('--root')\n100%|███████████████████████████████████████████████|\n29/29 [00:02<00:00, 10.17it/s]\nPlease do not work in internal in_* channels\n\nIf you like to rename the new work channel call:\n\npijul channel rename work_3bc7b1e $new_name\n\n$> pijul channel\n  in_3bc7b1e8618681d4e3069989160998f7d366f08c\n  main\n* work_3bc7b1e\n\n$> git pull\nUpdating 3bc7b1e..7ec741d\nFast-forward\n README.md      |  2 +-\n git_pijul.py   | 50 ++++++++++++++++++++++++++++++++++++++------------\n pyproject.toml |  2 +-\n 3 files changed, 40 insertions(+), 14 deletions(-)\n \n$> git pijul update\nUsing head: 7ec741d2e7b8c5c0ef7302d47e1b8af04c14b54d (master)\nUsing base from previous update: 3bc7b1e8618681d4e3069989160998f7d366f08c\n100%|███████████████████████████████████████████████| 1/1 [00:00<00:00,  8.20it/s]\nPlease do not work in internal in_* channels\n\nIf you like to rename the new work channel call:\n\npijul channel rename work_7ec741d $new_name\n\n$> pijul channel\n  in_3bc7b1e8618681d4e3069989160998f7d366f08c\n  in_7ec741d2e7b8c5c0ef7302d47e1b8af04c14b54d\n  main\n  work_3bc7b1e\n* work_7ec741d\n```\n\nchanges\n-------\n\n### 0.3.0\n\n* 0.3.0 git-pijul now creates a work and an internal channel. The internal\n  channel should not be used by the user. I think this is the first step to allow\n  back-sync.\n\n### 0.4.0\n\n* stop using .ignore, instead add root directory items one by one, ignoring .git\n\n### 0.5.0\n\n* allow to plot changes with `git pijul plot | dot -Txlib`\n \n### 0.6.0\n\n* `git-pijul plot` plots dependencies of all changes, with `-i` you can exclude changes from a\n  channel, usually the `main` channel that contains published changes. This allows\n  you to select the changes you want to publish.\n",
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
