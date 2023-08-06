# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['apteryx_transformers',
 'apteryx_transformers.models',
 'apteryx_transformers.parsers',
 'apteryx_transformers.simulated_annealing',
 'apteryx_transformers.simulated_annealing.heuristics',
 'apteryx_transformers.utils']

package_data = \
{'': ['*']}

install_requires = \
['dill>=0.3.4,<0.4.0',
 'fuzzysearch>=0.7.3,<0.8.0',
 'fuzzywuzzy>=0.18.0,<0.19.0',
 'matplotlib>=3.4.2,<4.0.0',
 'numpy>=1.21.1,<2.0.0',
 'scikit-learn>=0.24.2,<0.25.0',
 'scipy>=1.7.0,<2.0.0',
 'sentence-transformers>=2.0.0,<3.0.0',
 'setuptools>=57.4.0,<58.0.0',
 'torch>=1.9.0,<2.0.0',
 'torchaudio>=0.9.0,<0.10.0',
 'torchvision>=0.10.0,<0.11.0',
 'tqdm>=4.61.2,<5.0.0',
 'transformers>=4.9.1,<5.0.0']

setup_kwargs = {
    'name': 'apteryx-transformers',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'mgbvox',
    'author_email': 'mgbvox@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
