# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_breakword']

package_data = \
{'': ['*']}

install_requires = \
['breakword>=0.3.1,<0.4.0', 'pytest>=6.2.4,<7.0.0']

entry_points = \
{'pytest11': ['breakword = pytest_breakword.main']}

setup_kwargs = {
    'name': 'pytest-breakword',
    'version': '0.1.0',
    'description': 'Use breakword with pytest',
    'long_description': None,
    'author': 'Olivier Breuleux',
    'author_email': 'breuleux@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
