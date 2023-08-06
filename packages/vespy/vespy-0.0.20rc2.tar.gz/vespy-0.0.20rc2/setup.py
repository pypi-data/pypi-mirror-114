# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vespy']

package_data = \
{'': ['*'], 'vespy': ['certificates/*']}

install_requires = \
['certifi>=2021.5.30,<2022.0.0', 'requests>=2.26.0,<3.0.0']

entry_points = \
{'console_scripts': ['vespy = vespy.main:run']}

setup_kwargs = {
    'name': 'vespy',
    'version': '0.0.20rc2',
    'description': '"A small utility package',
    'long_description': None,
    'author': 'emher',
    'author_email': 'emher@vestas.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
