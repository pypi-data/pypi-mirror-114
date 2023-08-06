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
['Shapely>=1.7.1,<2.0.0',
 'anndata>=0.7.6,<0.8.0',
 'astropy>=4.3.post1,<5.0',
 'datashader>=0.13.0,<0.14.0',
 'geopandas>=0.9.0,<0.10.0',
 'ipywidgets>=7.6.3,<8.0.0',
 'leidenalg>=0.8.7,<0.9.0',
 'matplotlib>=3.4.2,<4.0.0',
 'numpy>=1.21.1,<2.0.0',
 'pandas>=1.3.1,<2.0.0',
 'proplot>=0.7.0,<0.8.0',
 'pygeos>=0.10.1,<0.11.0',
 'rasterio>=1.2.6,<2.0.0',
 'scanpy>=1.8.1,<2.0.0',
 'scipy>=1.7.0,<2.0.0',
 'seaborn>=0.11.1,<0.12.0',
 'skorch>=0.10.0,<0.11.0',
 'torchvision>=0.10.0,<0.11.0',
 'tqdm>=4.61.2,<5.0.0',
 'umap-learn>=0.5.1,<0.6.0']

setup_kwargs = {
    'name': 'bento-tools',
    'version': '0.1.1',
    'description': 'A toolkit for subcellular analysis of RNA organization',
    'long_description': '# Bento\n\nBento is a toolkit for ingesting, visualizing, and analyzing spatial transcriptomics data at subcellular resolution. \n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install bento.\n\n```bash\npip install bento-tools\n```\n\n## Usage\n\n```python\nimport bento\n# Todo\n```\n\n## Contributing\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\n## License\n[MIT](https://choosealicense.com/licenses/mit/)',
    'author': 'Clarence Mah',
    'author_email': 'ckmah@ucsd.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
