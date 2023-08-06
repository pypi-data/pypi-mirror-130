# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['chat_webhooks']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0', 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'chat-webhooks',
    'version': '1.0.0',
    'description': 'Interact and easily use Google Chat room webhooks.',
    'long_description': '# Python Template\n\nThis is a template that I plan on using for all of my future Python projects. The rest of this README will be filled out with sections that should be covered in any project.\n',
    'author': 'BD103',
    'author_email': 'dont@stalk.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://bd103.github.io',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
