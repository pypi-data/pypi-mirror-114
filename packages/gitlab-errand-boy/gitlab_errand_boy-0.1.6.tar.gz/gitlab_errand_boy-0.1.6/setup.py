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
    'version': '0.1.6',
    'description': 'Run errands with GitLab.',
    'long_description': '# gitlab_errand_boy\n\n### Usage\n\n```python\nimport gitlab_errand_boy\n\n\ncompounder = gitlab_errand_boy.Compounder(\n    project_id="23609881",\n    api_token="3Tsfsbuk9464TrdtrNNd"\n)\n\n# Create compound MR from open MRs.\ncompounder.compound()\n```\n\n### Requirements\n\nRequires Python >= 3.9.\n',
    'author': 'Gleb Buzin',
    'author_email': 'qufiwefefwoyn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/buzin.gb/gitlab_errand_boy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
