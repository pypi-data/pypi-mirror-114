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
    'version': '3.11.0',
    'description': "Nim's Django Helpers",
    'long_description': None,
    'author': 'Guilhem Saurel',
    'author_email': 'guilhem.saurel@laas.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
