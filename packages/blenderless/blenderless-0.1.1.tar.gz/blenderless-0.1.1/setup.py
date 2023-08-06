# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['blenderless']

package_data = \
{'': ['*']}

install_requires = \
['bpy==2.91a0',
 'hydra-core>=1.0.7,<2.0.0',
 'imageio',
 'pillow',
 'trimesh>=3.9.24,<4.0.0',
 'xvfbwrapper>=0.2.9,<0.3.0']

setup_kwargs = {
    'name': 'blenderless',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.8',
}


setup(**setup_kwargs)
