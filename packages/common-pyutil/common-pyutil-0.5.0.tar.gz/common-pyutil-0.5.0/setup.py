# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['common_pyutil']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0']

entry_points = \
{'console_scripts': ['test = pytest:main']}

setup_kwargs = {
    'name': 'common-pyutil',
    'version': '0.5.0',
    'description': 'Some common python utility functions',
    'long_description': "# common-pyutil\nBunch of common utility functions I've used in various projects. This package provides a uniform interface to them.\n",
    'author': 'Akshay',
    'author_email': 'atavist13@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/akshaybadola/common-pyutil',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
