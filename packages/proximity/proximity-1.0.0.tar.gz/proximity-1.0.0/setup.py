# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['proximity', 'proximity.vendor']

package_data = \
{'': ['*']}

install_requires = \
['numpy', 'polliwog>=1.0.0,<2', 'rtree==0.9.7', 'scipy', 'vg>=2.0.0']

setup_kwargs = {
    'name': 'proximity',
    'version': '1.0.0',
    'description': 'Mesh proximity queries based on libspatialindex and rtree, extracted from Trimesh',
    'long_description': None,
    'author': 'Paul Melnikow',
    'author_email': 'github@paulmelnikow.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://proximity.readthedocs.io/en/stable/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
