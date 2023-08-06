# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vectorops', 'vectorops.projection', 'vectorops.utils']

package_data = \
{'': ['*']}

install_requires = \
['RelevanceAI[notebook]>=0.17.0,<0.18.0',
 'document-utils>=1.3.0,<2.0.0',
 'numpy>=1.21.3,<2.0.0',
 'pandas>=1.3.3,<2.0.0',
 'plotly>=5.3.1,<6.0.0',
 'scikit-learn>=1.0,<2.0',
 'scipy>=1.7.1,<2.0.0',
 'torch>=1.9.1,<2.0.0',
 'torchvision>=0.10.1,<0.11.0',
 'vectorhub[text-encoder-transformers]>=1.8.3,<2.0.0']

setup_kwargs = {
    'name': 'relevanceai-vectorops',
    'version': '0.1.1',
    'description': 'Vector Ops Exploration and Tooling',
    'long_description': None,
    'author': 'Charlene Leong',
    'author_email': 'charlene.leong@relevance.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
