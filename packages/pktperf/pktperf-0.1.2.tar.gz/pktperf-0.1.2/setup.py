# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pktperf']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'netaddr>=0.8.0,<0.9.0']

setup_kwargs = {
    'name': 'pktperf',
    'version': '0.1.2',
    'description': 'pktgen scripts tool',
    'long_description': None,
    'author': 'junka',
    'author_email': 'wan.junjie@foxmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/junka/pktperf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
