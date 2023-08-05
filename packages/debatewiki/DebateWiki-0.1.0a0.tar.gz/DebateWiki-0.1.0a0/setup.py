# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['DebateWiki', 'DebateWiki.cli']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.0.1,<4.0.0', 'schema>=0.7.4,<0.8.0', 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['DebateWiki = DebateWiki.__main__:main']}

setup_kwargs = {
    'name': 'debatewiki',
    'version': '0.1.0a0',
    'description': 'A wiki that only allows valid arguments to make it into its pages.',
    'long_description': '# Debate Wiki\nA wiki that only allows valid arguments to make it into its pages.\n',
    'author': 'Taven',
    'author_email': 'taven@outlook.in',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/OpenDebates/DebateWiki',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
