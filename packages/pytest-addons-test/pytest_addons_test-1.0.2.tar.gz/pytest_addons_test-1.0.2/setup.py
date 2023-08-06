# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_addons_test']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=6.2.4,<7.0.0']

entry_points = \
{'console_scripts': ['poetry = pytest_addons_test']}

setup_kwargs = {
    'name': 'pytest-addons-test',
    'version': '1.0.2',
    'description': '用于测试pytest的插件',
    'long_description': None,
    'author': 'lin',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
