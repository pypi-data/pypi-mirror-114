# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['django_cognito_jwt', 'django_cognito_jwt_rydra']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=2.8,<3.0',
 'decorator>=4.4.1,<5.0.0',
 'django>=2.0,<3.0',
 'djangorestframework>=3.11.0,<4.0.0',
 'pyjwt>=1.7.1,<2.0.0',
 'redis>=3.3.11,<4.0.0',
 'requests>=2.22.0,<3.0.0']

setup_kwargs = {
    'name': 'django-cognito-jwt-rydra',
    'version': '0.0.4',
    'description': 'Django backends for AWS Cognito JWT (Forked from django-cognito-jwt with some customizations)',
    'long_description': None,
    'author': 'David Jiménez',
    'author_email': 'davigetto@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rydra/django-cognito-jwt',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
