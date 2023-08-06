# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hobart']

package_data = \
{'': ['*']}

install_requires = \
['numpy', 'polliwog>=1.0.0,<2', 'scipy', 'vg>=2.0.0']

setup_kwargs = {
    'name': 'hobart',
    'version': '1.0.0',
    'description': 'Obtain cross sections of polygonal meshes',
    'long_description': None,
    'author': 'Paul Melnikow',
    'author_email': 'github@paulmelnikow.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://hobart.readthedocs.io/en/stable/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
