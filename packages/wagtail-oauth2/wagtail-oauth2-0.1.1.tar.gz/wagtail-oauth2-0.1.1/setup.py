# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['wagtail_oauth2', 'wagtail_oauth2.tests']

package_data = \
{'': ['*'], 'wagtail_oauth2': ['templates/*']}

install_requires = \
['Django>=3.2.4,<4.0.0', 'requests>=2.26.0,<3.0.0', 'wagtail>=2.14.1,<3.0.0']

setup_kwargs = {
    'name': 'wagtail-oauth2',
    'version': '0.1.1',
    'description': 'OAuth2.0 authentication fo wagtail',
    'long_description': 'Wagtail OAuth2.0 Login\n======================\n\nPlugin to replace Wagtail Login by an OAuth2.0 Authorization Server.\n',
    'author': 'Guillaume Gauvrit',
    'author_email': 'guillaume@gandi.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
