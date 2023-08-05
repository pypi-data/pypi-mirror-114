# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['github_traffic']
install_requires = \
['PyGithub>=1.43.8',
 'click-aliases>=1.0.1,<2.0.0',
 'click>=7',
 'terminaltables>=3.1.0,<4.0.0']

entry_points = \
{'console_scripts': ['github-traffic = github_traffic:cli']}

setup_kwargs = {
    'name': 'github-traffic',
    'version': '0.2.0',
    'description': 'Summarize Github traffic stats across repositories.',
    'long_description': '|pypi-badge|\n\ngithub-traffic\n==============\n\nSummarize Github traffic stats across repos\n\n\nInstall\n-------\n\nLatest stable::\n\n  $ pip install --user github-traffic\n\nLatest pre-release::\n\n  $ pip install --user --pre github-traffic\n\nGit::\n\n  $ pip install --user git+https://github.com/jashandeep-sohi/github-traffic.git\n\nUsage\n-----\n\nViews & clones summary::\n\n  $ github-traffic --token "$GITHUB_TOKEN" summary\n\nViews summary::\n\n  $ github-traffic --token "$GITHUB_TOKEN" summary --metrics views\n\nClones summary::\n\n  $ github-traffic --token "$GITHUB_TOKEN" summary --metrics clones\n\nTop referrers::\n\n  $ github-traffic --token "$GITHUB_TOKEN" referrers\n\nTop paths::\n\n  $ github-traffic --token "$GITHUB_TOKEN" paths\n\n.. |pypi-badge| image:: https://img.shields.io/pypi/v/github-traffic\n    :alt: PyPI\n    :target: https://pypi.org/project/github-traffic/\n',
    'author': 'Jashandeep Sohi',
    'author_email': 'jashandeep.s.sohi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jashandeep-sohi/github-traffic',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
