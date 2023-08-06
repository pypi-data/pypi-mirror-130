# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['relycomply_client']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML',
 'Pygments',
 'boto3',
 'gql==3.0.0a1',
 'littleutils',
 'pandas',
 'pyarrow',
 'requests',
 'requests-toolbelt',
 'tabulate',
 'termcolor',
 'toml']

entry_points = \
{'console_scripts': ['rely = relycomply_client.cli:main']}

setup_kwargs = {
    'name': 'relycomply-client',
    'version': '0.7.0',
    'description': 'A python client for the RelyComply platform',
    'long_description': '# RelyComply Python Client and CLI\n\n**BETA RELEASE**\n\nThis package contains the python client and CLI for the RelyComply platform:\n\n> RelyComply is an end-to-end Anti-Money Laundering (AML) Plaftorm, managing detection, risk management and automation of your AML compliance requirements\n\nThe CLI makes configuration of the system substantially simpler and allows for a full configuration-as-devops experience. \n\nThe python client exposes both a lower level GraphQL client which makes it easy to interact with the GraphQL APi in a pythonic manner. As well as a higher-level integration client that provides useful routines for common integration tasks.\n\n## RelyComplyGQLClient\n\nA flexible and intelligent GraphQL client for RelyComply. This client will create methods\nthat match the mutation sand queries of the RelyComply API, and expose them with familiar\ncalling conventions. It also handles paging as well as simplifying the returned structures.\n\nQueries can be called with their lowerCase field name and any filter arguments as kwargs, e.g.:\n\n```python\nclient.products(nameContain="ZA") # Will return a list of products\nclient.products(nameContain="ZA", _iter=True) # Will return a lazy generator\nclient.products(name="retailZA", _only=True) # Will return only the first object or None\n```\n\nMutations can be called in a similar way, but arguments will be lifted into the $input variable\n\n```python\nclient.createProduct(name="retailZA", label="South African Retail) # Returns the created product\n```\n\nThe interface is automatically generated from the GQL schema as well as the CLI support templates. Thus it should always be in sync with the latest features on the platform.\n\n## RelyComplyClient\n\n## CLI\n',
    'author': 'James Saunders',
    'author_email': 'james@relycomply.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.relycomply.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
