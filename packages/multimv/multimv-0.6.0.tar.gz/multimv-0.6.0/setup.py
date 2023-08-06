# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['multimv', 'multimv.vendor.toposort']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0']

entry_points = \
{'console_scripts': ['multimv = multimv:main']}

setup_kwargs = {
    'name': 'multimv',
    'version': '0.6.0',
    'description': 'Multi mv via fixed string / regex / bash pattern substitutions',
    'long_description': None,
    'author': 'Summer',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
