# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['last9', 'last9.wsgi']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.0.2,<3.0.0',
 'Werkzeug>=2.0.2,<3.0.0',
 'prometheus-client>=0.11.0,<0.12.0']

setup_kwargs = {
    'name': 'last9',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
