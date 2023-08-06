# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bento',
 'bento.datasets',
 'bento.io',
 'bento.plotting',
 'bento.preprocessing',
 'bento.tests',
 'bento.tools']

package_data = \
{'': ['*'], 'bento': ['models/spots/five_pattern/*', 'models/spots/pattern/*']}

install_requires = \
['anndata>=0.7.1,<0.8.0',
 'astropy>=4.0.1,<5.0.0',
 'datashader>=0.12,<0.13',
 'geopandas>=0.9.0,<0.10.0',
 'ipywidgets>=7.5.1,<8.0.0',
 'leidenalg>=0.8.3,<0.9.0',
 'matplotlib>=3.2.1,<4.0.0',
 'numpy>=1.18.4,<2.0.0',
 'pandas>=1.2.0,<2.0.0',
 'proplot>=0.6.4,<0.7.0',
 'pydata-sphinx-theme>=0.6.3,<0.7.0',
 'pygeos>=0.8,<0.9',
 'rasterio>=1.2.1,<2.0.0',
 'scanpy>=1.6.0,<2.0.0',
 'scikit-learn>=0.22.2.post1,<0.23.0',
 'scipy>=1.4.1,<2.0.0',
 'seaborn>=0.11.0,<0.12.0',
 'shapely>=1.7.0,<2.0.0',
 'skorch>=0.9.0,<0.10.0',
 'torchvision>=0.8.1,<0.9.0',
 'tqdm>=4.44.1,<5.0.0']

setup_kwargs = {
    'name': 'bento-tools',
    'version': '0.1.0',
    'description': 'A toolkit for subcellular analysis of RNA organization',
    'long_description': None,
    'author': 'Clarence Mah',
    'author_email': 'ckmah@ucsd.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0',
}


setup(**setup_kwargs)
