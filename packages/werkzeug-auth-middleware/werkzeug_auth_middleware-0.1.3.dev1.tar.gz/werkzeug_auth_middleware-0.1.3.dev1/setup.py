# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['werkzeug_auth_middleware']

package_data = \
{'': ['*']}

install_requires = \
['Werkzeug==2.0.1', 'requests==2.26.0']

setup_kwargs = {
    'name': 'werkzeug-auth-middleware',
    'version': '0.1.3.dev1',
    'description': '',
    'long_description': None,
    'author': 'sorxcode',
    'author_email': 'sorxcode@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
