# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_telegram_bot_django_persistence',
 'python_telegram_bot_django_persistence.migrations']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.1', 'python-telegram-bot>=13.7']

setup_kwargs = {
    'name': 'python-telegram-bot-django-persistence',
    'version': '0.1.4',
    'description': 'Package to use Django ORM as persistence engine in Python Telegram Bot',
    'long_description': '# python-telegram-bot-django-persistence\nPackage to use Django ORM as persistence engine in Python Telegram Bot\n',
    'author': 'Alexander Shishenko',
    'author_email': 'alex@shishenko.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/GamePad64/python-telegram-bot-django-persistence',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
