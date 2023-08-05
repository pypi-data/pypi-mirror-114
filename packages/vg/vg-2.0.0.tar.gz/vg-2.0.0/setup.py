# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vg', 'vg.compat']

package_data = \
{'': ['*']}

install_requires = \
['numpy']

setup_kwargs = {
    'name': 'vg',
    'version': '2.0.0',
    'description': 'Linear algebra for humans: a very good vector-geometry and linear-algebra toolbelt',
    'long_description': None,
    'author': 'Paul Melnikow',
    'author_email': 'github@paulmelnikow.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://vgpy.readthedocs.io/en/stable',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
