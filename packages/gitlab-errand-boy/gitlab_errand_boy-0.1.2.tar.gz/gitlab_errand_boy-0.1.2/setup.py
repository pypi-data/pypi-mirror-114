# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gitlab_errand_boy']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0', 'tenacity>=6.1.0']

setup_kwargs = {
    'name': 'gitlab-errand-boy',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Gleb Buzin',
    'author_email': 'qufiwefefwoyn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
