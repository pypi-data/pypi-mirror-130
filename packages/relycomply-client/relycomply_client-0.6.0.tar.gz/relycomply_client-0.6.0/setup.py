# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['relycomply_client']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'Pygments>=2.10.0,<3.0.0',
 'boto3',
 'gql==3.0.0a1',
 'littleutils',
 'pandas',
 'pyarrow>=6.0.1,<7.0.0',
 'requests',
 'requests-toolbelt',
 'tabulate>=0.8.9,<0.9.0',
 'termcolor>=1.1.0,<2.0.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['rely = relycomply_client.cli:main']}

setup_kwargs = {
    'name': 'relycomply-client',
    'version': '0.6.0',
    'description': 'A python client for the RelyComply platform',
    'long_description': None,
    'author': 'James Saunders',
    'author_email': 'james@relycomply.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
