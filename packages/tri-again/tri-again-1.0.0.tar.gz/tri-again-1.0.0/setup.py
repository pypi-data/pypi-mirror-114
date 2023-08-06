# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tri_again']

package_data = \
{'': ['*']}

install_requires = \
['numpy',
 'polliwog>=1.0.0,<2',
 'pycollada>=0.7.1,<0.8',
 'toolz>=0.10.0,<0.12.0',
 'vg>=2.0.0',
 'webcolors>=1.11.1,<2']

setup_kwargs = {
    'name': 'tri-again',
    'version': '1.0.0',
    'description': 'Scenegraph for quickly debugging 3D meshes, polylines, and points',
    'long_description': None,
    'author': 'Paul Melnikow',
    'author_email': 'github@paulmelnikow.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lace/tri-again',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.9',
}


setup(**setup_kwargs)
