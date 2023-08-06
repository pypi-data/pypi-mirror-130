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
    'version': '1.0.1',
    'description': 'Interact and easily use Google Chat room webhooks.',
    'long_description': '# Chat Webhooks\n\nEasily interact and send messages with Google Chat\'s webhooks feature. This API is small, but should be a nice framework for working with any webhook.\n\n## Installation\n\n```shell\npython -m pip install -U chat_webhooks\n```\n\n## Getting Started\n\n```python\n# API Example\nfrom chat_webhooks import ChatWebhook\n\nchat = ChatWebhook("WEBHOOK_URL")\nchat.send("Hello, world!")\n```\n\n```shell\n# Shell example\n$ python -m chat_webhooks -w "WEBHOOK_URL"\n\n# Interactive Google Chat webhook client\n# Made by BD103\n\n> Hello, world!\n```\n\n## More Documentation\n\nYou can view a short guide [here](https://bd103.github.io/Chat-Webhooks).\n',
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
