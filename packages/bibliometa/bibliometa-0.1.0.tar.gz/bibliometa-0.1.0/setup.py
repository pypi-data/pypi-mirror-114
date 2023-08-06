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
 'flake8>=3.9.2,<4.0.0',
 'geopandas>=0.9.0,<0.10.0',
 'loguru>=0.5.3,<0.6.0',
 'matplotlib>=3.4.2,<4.0.0',
 'networkx>=2.6.1,<3.0.0',
 'pandas>=1.3.0,<2.0.0',
 'scipy>=1.7.0,<2.0.0',
 'tqdm>=4.61.2,<5.0.0']

extras_require = \
{':extra == "docs"': ['sphinx>=4.1.2,<5.0.0', 'sphinx-rtd-theme>=0.5.2,<0.6.0']}

setup_kwargs = {
    'name': 'bibliometa',
    'version': '0.1.0',
    'description': 'A package for manipulating, converting and analysing bibliographic metadata',
    'long_description': None,
    'author': 'Andreas Lüschow',
    'author_email': 'lueschow@sub.uni-goettingen.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
