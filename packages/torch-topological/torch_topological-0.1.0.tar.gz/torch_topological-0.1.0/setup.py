# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['torch_topological',
 'torch_topological.demos',
 'torch_topological.nn',
 'torch_topological.utils']

package_data = \
{'': ['*']}

install_requires = \
['giotto-ph>=0.2.0,<0.3.0',
 'giotto-tda>=0.5.1,<0.6.0',
 'matplotlib>=3.5.0,<4.0.0',
 'torch>=1.10.0,<2.0.0']

setup_kwargs = {
    'name': 'torch-topological',
    'version': '0.1.0',
    'description': 'A framework for topological machine learning based on `pytorch`.',
    'long_description': '<img src="torch_topological.svg" height=128 alt="`pytorch-topological` icon" />\n\n# `pytorch-topological`: A topological machine learning framework for `pytorch`\n\n`pytorch-topological` (or `torch_topological`) is a topological machine\nlearning framework for [PyTorch](https://pytorch.org). It aims to\ncollect *loss terms* and *neural network layers* in order to simplify\nbuilding the next generation of topology-based machine learning tools.\n\n`torch_topological` is still a work in progress. Stay tuned for more\ninformation.\n\n# Installation\n\nIt is recommended to use the excellent [`poetry`](https://python-poetry.org) framework\nto install `torch_topological`:\n\n```\npoetry add torch-topological\n```\n\nAlternatively, use `pip` to install the package:\n\n```\npip install -U torch-topological\n```\n\n# Dependencies\n\n`torch_topological` is making heavy use of [`giotto-ph`](https://github.com/giotto-ai/giotto-ph),\na high-performance implementation of [`Ripser`](https://github.com/Ripser/ripser).\n',
    'author': 'Bastian Rieck',
    'author_email': 'bastian@rieck.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
