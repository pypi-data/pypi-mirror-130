# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['i_lazy',
 'i_lazy.data_structures',
 'i_lazy.data_structures.dict',
 'i_lazy.utils']

package_data = \
{'': ['*']}

install_requires = \
['flatdict>=4.0.1,<5.0.0']

setup_kwargs = {
    'name': 'i-lazy',
    'version': '0.1.1',
    'description': 'A small collection of Python laziness.',
    'long_description': None,
    'author': 'Peter Yuen',
    'author_email': 'ppeetteerrsx@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ppeetteerrs/i-lazy-python.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
