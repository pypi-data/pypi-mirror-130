# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['itchat', 'itchat.async_components', 'itchat.components', 'itchat.storage']

package_data = \
{'': ['*']}

install_requires = \
['PyQRCode>=1.2.1,<2.0.0', 'pypng>=0.0.21,<0.0.22', 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'itchat2-uos',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'aox.lei',
    'author_email': '2387813033@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
