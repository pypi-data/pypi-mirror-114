# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['git_pijul']
install_requires = \
['click>=8.0.1', 'temppathlib>=1.1.0', 'toml>=0.10.2', 'tqdm>=4.61.2']

entry_points = \
{'console_scripts': ['git-pijul = git_pijul:main']}

setup_kwargs = {
    'name': 'git-pijul',
    'version': '0.9.2',
    'description': 'update pijul from git',
    'long_description': "git-pijul\n=========\n\nupdate pijul from git.\n\ninstall\n-------\n\n```bash\npip install git-pijul\n```\n\nusage\n-----\n\n```text\nUsage: git-pijul [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  create            Create a new pijul repository and import a linear...\n  plot              Display current changes as graphviz file (git pijul...\n  set-diff          Difference between two sets of changes of channels.\n  set-intersection  Intersection between two sets of changes of channels.\n  set-union         Union changes of channels.\n  shallow           create a new pijul repository from the current...\n  update            Update a repository created with git-pijul\n```\n\n`git-pijul create` finds an ancestry-path with `git rev-list --ancestry-path\n--no-merges --topo-order`. It will then checkout each revision into a temp\ndirectory and add it to pijul. Non-linear history is dropped. The last\nrevision/patchset will be forked into a channel.\n\n`git-pijul update` finds in git the shortest path from the current git-revision\nto a existing channel and updates pijul from that channel.\n\n`git-pijul shallow` create a new pijul repository from the current revision without\nhistory.\n\n`git-pijul plot` plots dependencies of all changes, with `-i` you can exclude changes from a\nchannel, usually the `main` channel that contains published changes. This allows\nyou to select the changes you want to publish.\n\nThere are also set opertions on sets of changes in channels. Typical usage is\napplying changes after a `git pijul update`:\n\n```bash\ngit pijul set-diff -l  work_9189af5 | xargs pijul apply\n```\n\nexample\n-------\n\n```console\n$> git clone https://github.com/ganwell/git-pijul\nCloning into 'git-pijul'...\nremote: Enumerating objects: .....\n\n$> cd git-pijul\n\n$> git pijul create --name upsteam01\nUsing head: e75db07f2b56b1a836f3841808b188ea8e642ba1 (HEAD)\nUsing base: b215e32b5d60eb19a0676a2b9072ac7a352e1c50 ('--root')\n100%|█████████████████████████████████████| 40/40 [00:03<00:00, 12.40it/s]\nPlease do not modify the in_* channels\n\nTo get the latest changes call:\n\ngit pijul set-diff -l upstream01 | xargs pijul apply\n\n$> git pijul set-diff -l upstream01 | xargs pijul apply\nOutputting repository ↖\n\n$> pijul channel\n  in_e75db07f2b56b1a836f3841808b188ea8e642ba1\n* main\n  upstream01\n\n$> git pull\nUpdating 3bc7b1e..7ec741d\nFast-forward\n README.md      |  2 +-\n git_pijul.py   | 50 ++++++++++++++++++++++++++++++++++++++------------\n pyproject.toml |  2 +-\n 3 files changed, 40 insertions(+), 14 deletions(-)\n\n$> git pijul update --name upstream02\nUsing head: 2386120d310e65ea38110059fc427c106a75a58a (master)\nUsing base from previous update: e75db07f2b56b1a836f3841808b188ea8e642ba1\n100%|█████████████████████████████████████| 7/7 [00:00<00:00,  7.62it/s]\nPlease do not modify the in_* channels\n\nTo get the latest changes call:\n\ngit pijul set-diff -l upstream02 | xargs pijul apply\n\n$> git pijul set-diff -l upstream02 | xargs pijul apply\nOutputting repository ↖\n\n$> pijul channel\n  in_e75db07f2b56b1a836f3841808b188ea8e642ba1\n  in_2386120d310e65ea38110059fc427c106a75a58a\n* main\n  upstream01\n  upstream02\n```\n\nFrom 0.9.0 on you can also use:\n\n```python\ngit pijul apply upstream02\n```\n\nchanges\n-------\n\n### 0.3.0\n\n* 0.3.0 git-pijul now creates a work and an internal channel. The internal\n  channel should not be used by the user. I think this is the first step to allow\n  back-sync.\n\n### 0.4.0\n\n* stop using .ignore, instead add root directory items one by one, ignoring .git\n\n### 0.5.0\n\n* allow to plot changes with `git pijul plot | dot -Txlib`\n\n### 0.6.0\n\n* `git-pijul plot` plots dependencies of all changes, with `-i` you can exclude changes from a\n  channel, usually the `main` channel that contains published changes. This allows\n  you to select the changes you want to publish.\n\n### 0.7.0\n\n* add set operations on changes in channels\n\n### 0.8.0\n\n* do not switch channels, use --channel for all operations\n\n### 0.9.0\n\n* add command to apply changes from channel iteratively\n",
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
