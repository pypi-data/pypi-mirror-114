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
    'version': '0.1.2',
    'description': 'Blenderless is the python package for easy headless rendering using blender.',
    'long_description': "# Blenderless\n\nBlenderless is the python package for easy headless rendering using blender.\n\n\n## Getting Started\n\nCreate image from mesh:\n\n```python\nimport blenderless\npath_to_foo_png = blenderless.render('foo.stl')\n```\n\n### Installing\n\nInstall blenderless\n```buildoutcfg\nsudo apt-get install xvfb pipx\npipx install poetry==1.1.5\nmake .venv\n```\n\n### Running the tests\n\n```sh\nmake test\n```\n",
    'author': 'Axel Vlaminck',
    'author_email': 'axel.vlaminck@oqton.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/oqton/blenderless',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.8',
}


setup(**setup_kwargs)
