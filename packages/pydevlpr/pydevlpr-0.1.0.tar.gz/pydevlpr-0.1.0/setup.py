# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pydevlpr']

package_data = \
{'': ['*']}

install_requires = \
['websockets>=9.1,<10.0']

setup_kwargs = {
    'name': 'pydevlpr',
    'version': '0.1.0',
    'description': 'Frontend for connecting to devlprd and processing data from a FANTM DEVLPR',
    'long_description': None,
    'author': 'Ezra Boley',
    'author_email': 'eboley@wisc.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
