# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['audible_series']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0', 'audible>=0.5.4,<0.6.0']

entry_points = \
{'audible.cli_plugins': ['series = audible_series.cmd_series:cli']}

setup_kwargs = {
    'name': 'audible-series',
    'version': '1.0.0',
    'description': 'Look for new series realeases in Audible',
    'long_description': None,
    'author': 'Alex Lusco',
    'author_email': 'alex.lusco@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
