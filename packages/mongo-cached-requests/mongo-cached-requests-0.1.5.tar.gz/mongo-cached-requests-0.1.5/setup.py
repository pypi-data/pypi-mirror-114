# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mongo_cached_requests']

package_data = \
{'': ['*']}

install_requires = \
['pymongo>=3.11.4,<4.0.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'mongo-cached-requests',
    'version': '0.1.5',
    'description': '',
    'long_description': None,
    'author': 'Patrick Fenerty',
    'author_email': 'patrick@fenerty.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
