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
    'version': '1.0.1',
    'description': "Adds a command to audible-cli that looks for new series releases in a user's library.",
    'long_description': '# Audible Series Command\n\nCan be used to print out series that are coming up next from a poetry shell.\n\n```\npoetry shell\naudible library export\naudible series -l $PWD/library.csv -c $PWD/config.yaml\n```\n\nThe config file is optional but can be used to override book data in cases where\na book is already preordered, a series should be ignored, or if audible data is\nbad.  It can also be used to manually set a case where a book was read somewhere\nelse but it is not in your library (though this requires manually looking up the\naudible ASIN).\n\nNote: While the packaging of all this will automatically just work when\ninstalled with pip the audible-cli itself is not in pypi.  You must clone the\ngit repo https://github.com/mkb79/audible-cli then pip install this repo for the\naudible cli to be usable.\n',
    'author': 'Alex Lusco',
    'author_email': 'alex.lusco@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/luscoma/audible-series',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
