# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['apitestbasic', 'apitestbasic.GraphqlApi', 'apitestbasic.User']

package_data = \
{'': ['*']}

install_requires = \
['sgqlc>=13.0,<14.0']

setup_kwargs = {
    'name': 'apitestbasic',
    'version': '0.2.4',
    'description': '',
    'long_description': None,
    'author': 'lin',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
