# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nornir_akamai',
 'nornir_akamai.plugins',
 'nornir_akamai.plugins.connections',
 'nornir_akamai.plugins.tasks',
 'nornir_akamai.plugins.tasks.v1']

package_data = \
{'': ['*']}

install_requires = \
['edgegrid-python>=1.2.1,<2.0.0',
 'nornir>=3.0.0,<4.0.0',
 'packaging>=20.9,<21.0',
 'requests-toolbelt>=0.9.1,<0.10.0',
 'urllib3>=1.26.3,<2.0.0']

entry_points = \
{'nornir.plugins.connections': ['akamai = '
                                'nornir_akamai.plugins.connections:AkamaiRestClient']}

setup_kwargs = {
    'name': 'nornir-akamai',
    'version': '0.0.1',
    'description': 'Akamai plugins for Nornir',
    'long_description': '# nornir_akamai\n\nCollection of Nornir plugins to interact with Akamai REST API and manage GTM objects through CRUD operations.\n\n## Installation\n\n### Pip\n\n```bash\npip install nornir-akamai\n```\n\n### Poetry\n\n```bash\npoetry add nornir-akamai\n```\n\n## Usage\n\n## Plugins\n\n### Connections\n\n\n## Authors\n\n* Kevin Pressouyre (@kpressouyre)',
    'author': 'Kevin Pressouyre',
    'author_email': 'kevin.pressouyre@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kpressouyre/nornir_akamai',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
