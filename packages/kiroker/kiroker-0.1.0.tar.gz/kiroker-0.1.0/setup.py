# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kiroker']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0']

setup_kwargs = {
    'name': 'kiroker',
    'version': '0.1.0',
    'description': 'A changelog generator.',
    'long_description': None,
    'author': 'Ryosuke Imai',
    'author_email': 'imai@qunasys.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
