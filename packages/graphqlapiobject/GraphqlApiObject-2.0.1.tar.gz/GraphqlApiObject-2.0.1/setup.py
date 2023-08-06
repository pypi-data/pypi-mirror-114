# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['graphqlapiobject', 'graphqlapiobject.GraphqlApi', 'graphqlapiobject.User']

package_data = \
{'': ['*']}

install_requires = \
['PyHamcrest>=2.0.2,<3.0.0',
 'beeprint>=2.4.10,<3.0.0',
 'jmespath>=0.10.0,<0.11.0',
 'pytest>=6.2.4,<7.0.0',
 'python-utils>=2.5.6,<3.0.0',
 'sgqlc>=13.0,<14.0']

setup_kwargs = {
    'name': 'graphqlapiobject',
    'version': '2.0.1',
    'description': '用于测试graphql的接口，依赖于sgqlc',
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
