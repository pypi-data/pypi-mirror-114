# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymongo_the_sql']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pymongo-the-sql',
    'version': '0.0.1',
    'description': 'A sql wrapper made to mimic the pymongo syntax in order to simplify sql syntax.',
    'long_description': None,
    'author': 'Marcus Bader',
    'author_email': 'marcus@appsight.se',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
