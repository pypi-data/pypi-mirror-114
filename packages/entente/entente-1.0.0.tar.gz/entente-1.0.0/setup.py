# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['entente', 'entente.landmarks']

package_data = \
{'': ['*']}

install_requires = \
['cached_property',
 'lacecore[obj]>=1.0.0,<2',
 'meshlab-pickedpoints>=2.0.0,<3',
 'numpy<1.19.0',
 'ounce>=1.1.1,<2.0',
 'polliwog>=1.0.0,<2.0',
 'scipy',
 'tqdm',
 'vg>=2.0.0']

extras_require = \
{'cli': ['click>7.0,<9.0', 'PyYAML>=5.1', 'tri-again>=1.0.0,<2.0'],
 'landmarker': ['proximity>=1.0.0,<2']}

setup_kwargs = {
    'name': 'entente',
    'version': '1.0.0',
    'description': 'Polygonal meshes in vertex-wise correspondence',
    'long_description': None,
    'author': 'Paul Melnikow',
    'author_email': 'github@paulmelnikow.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lace/entente',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<3.9',
}


setup(**setup_kwargs)
