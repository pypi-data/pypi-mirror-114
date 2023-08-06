# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['info_ut', 'info_ut.feed']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=21.2.0,<22.0.0',
 'beautifulsoup4>=4.9.3,<5.0.0',
 'feedparser>=6.0.8,<7.0.0',
 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'info-ut',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'hexatester',
    'author_email': 'revolusi147id@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
