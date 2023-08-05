# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ndh', 'ndh.templatetags']

package_data = \
{'': ['*'],
 'ndh': ['static/css/*',
         'templates/*',
         'templates/ndh/*',
         'templates/registration/*']}

install_requires = \
['django-autoslug>=1.9.8,<2.0.0', 'django-bootstrap4>=2.3.1,<3.0.0']

setup_kwargs = {
    'name': 'ndh',
    'version': '3.11.1',
    'description': "Nim's Django Helpers",
    'long_description': "# Nim's Django Helpers\n\n[![Documentation Status](https://readthedocs.org/projects/ndh/badge/?version=latest)](https://ndh.readthedocs.io/en/latest/?badge=latest)\n[![PyPI version](https://badge.fury.io/py/ndh.svg)](https://pypi.org/project/ndh)\n[![Tests](https://github.com/nim65s/ndh/actions/workflows/test.yml/badge.svg)](https://github.com/nim65s/ndh/actions/workflows/test.yml)\n[![codecov](https://codecov.io/gh/nim65s/ndh/branch/master/graph/badge.svg?token=BLGISGCYKG)](https://codecov.io/gh/nim65s/ndh)\n[![Maintainability](https://api.codeclimate.com/v1/badges/6737a84239590ddc0d1e/maintainability)](https://codeclimate.com/github/nim65s/ndh/maintainability)\n\n## Requirements\n\n- Python 3.6+\n- Django 2.0+\n- [django-autoslug](https://github.com/justinmayer/django-autoslug)\n- [django-bootstrap4](https://github.com/zostera/django-bootstrap4)\n\n## Install\n\n`pip install ndh`\n",
    'author': 'Guilhem Saurel',
    'author_email': 'guilhem.saurel@laas.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nim65s/ndh',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
