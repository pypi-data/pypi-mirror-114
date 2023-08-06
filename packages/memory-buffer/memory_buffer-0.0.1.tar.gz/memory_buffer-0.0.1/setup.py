# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['memory_buffer']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'memory-buffer',
    'version': '0.0.1',
    'description': 'This module will let you write debug messages into a 500MB memory buffer which is Circular.',
    'long_description': None,
    'author': 'Santhosh Balasa',
    'author_email': 'santhosh.kbr@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sbalasa/MemoryBuffer.git',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
