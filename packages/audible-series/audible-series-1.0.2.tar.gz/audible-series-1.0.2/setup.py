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
    'version': '1.0.2',
    'description': "Adds a command to audible-cli that looks for new series releases in a user's library.",
    'long_description': "# Audible Series Command\n\n## Installation\n\n```\npip3 install audible\npip3 install audible-series\n```\n\nSadly the audible-cli tool is not in pypi but is packaged, it's easiest to\ninstall via git:\n\n```\ngit clone https://github.com/mkb79/audible-cli\npip3 install ./audible-cli\n```\n\n## Usage\n\nThe command will work on an exported library file:\n\n```\naudible library export\naudible series -l $PWD/library.csv -c $PWD/config.yaml\n```\n\nThe config file is optional but can be used to override book data in cases where\na book is already preordered, a series should be ignored, or if audible data is\nbad.  It can also be used to manually set a case where a book was read somewhere\nelse but it is not in your library (though this requires manually looking up the\naudible ASIN).\n\n## Development\n\n\nThis project uses poetry which wraps a bunch of tools like virtualenv.  The\neasiest way to run it for development is to clone this repository then run a\npoetry shell.\n\n```\npoetry shell\naudible library export\naudible series -l $PWD/library.csv -c $PWD/config.yaml\n```\n\nWhen developing the `--only_series` flag may be useful since it will filter the\nlibrary to a single series.\n",
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
