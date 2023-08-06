# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['bibliometa', 'bibliometa.graph', 'bibliometa.utils']

package_data = \
{'': ['*']}

install_requires = \
['cartopy>=0.19.0,<0.20.0',
 'cython>=0.29.24,<0.30.0',
 'geopandas>=0.9.0,<0.10.0',
 'loguru>=0.5.3,<0.6.0',
 'matplotlib>=3.4.2,<4.0.0',
 'networkx>=2.6.1,<3.0.0',
 'numpy>=1.21.1,<2.0.0',
 'pandas>=1.3.0,<2.0.0',
 'scipy>=1.7.0,<2.0.0',
 'shapely>=1.7.1,<2.0.0',
 'tqdm>=4.61.2,<5.0.0']

setup_kwargs = {
    'name': 'bibliometa',
    'version': '0.1.1',
    'description': 'A package for manipulating, converting and analysing bibliographic metadata',
    'long_description': '# Bibliometa\n\n[![Documentation Status](https://readthedocs.org/projects/bibliometa/badge/?version=latest)](https://bibliometa.readthedocs.io/en/latest/?badge=latest)\n[![PyPI version](https://badge.fury.io/py/bibliometa.svg)](https://badge.fury.io/py/bibliometa)\n\nBibliometa is a python library for manipulating, converting and analysing bibliographic metadata, with a focus on graph analysis.\n\n*Repository*: https://github.com/alueschow/bibliometa\n\n*Package*: https://pypi.org/project/bibliometa/\n\n*License*: MIT\n\n-----\n\n## Installation\n* Use pip: ```pip install bibliometa```\n\n## Development\n* Clone this repository: ```git clone https://github.com/alueschow/bibliometa.git```\n* Run ```poetry install``` to install all necessary dependencies\n+ After development, run ```poetry export --without-hashes -f requirements.txt --output requirements.txt ``` to create a _requirements.txt_ file with all dependencies. This file is needed to create the documentation on [ReadTheDocs](https://readthedocs.org/).\n*  Run ```poetry run sphinx-apidoc -f -o source ../src/bibliometa``` and then ```poetry run make html``` from within the _docs_ folder to create a local documentation using [Sphinx](https://www.sphinx-doc.org/en/master/).\n',
    'author': 'Andreas Lüschow',
    'author_email': 'lueschow@sub.uni-goettingen.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://bibliometa.readthedocs.io',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
