# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['sloth_ci_val_github']
install_requires = \
['sloth-ci>=2.2,<3.0']

setup_kwargs = {
    'name': 'sloth-ci-val-github',
    'version': '1.1.1',
    'description': 'GitHub validator for Sloth CI',
    'long_description': '# GitHub Validator for Sloth CI\n\n\n## Installation\n    \n    $ pip install sloth-ci-val-github\n\n\n## Usage\n\n    provider:\n        github:\n            # Repository owner. Mandatory parameter.\n            owner: moigagoo\n\n            # Repository title as it appears in the URL, i.e. slug.\n            # Mandatory parameter.\n            repo: sloth-ci\n\n            # Only pushes to these branches will initiate a build.\n            # Skip this parameter to allow all branches to fire builds.\n            branches:\n                - master\n                - staging\n\n',
    'author': 'Constantine Molchanov',
    'author_email': 'moigagoo@live.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
