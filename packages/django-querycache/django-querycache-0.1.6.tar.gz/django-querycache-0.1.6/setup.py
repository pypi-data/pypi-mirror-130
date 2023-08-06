# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_querycache']

package_data = \
{'': ['*'],
 'django_querycache': ['.pytest_cache/*', '.pytest_cache/v/cache/*', 'cover/*']}

setup_kwargs = {
    'name': 'django-querycache',
    'version': '0.1.6',
    'description': 'Cache manager for Django querysets and serialization',
    'long_description': None,
    'author': 'Joshua Brooks',
    'author_email': 'josh.vdbroek@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
