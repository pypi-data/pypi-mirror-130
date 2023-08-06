# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['archivotron', 'archivotron.tests']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'archivotron',
    'version': '0.0.0rc0',
    'description': 'Scientific data archiving assistant',
    'long_description': None,
    'author': 'Joshua Teves',
    'author_email': 'joshua.teves@nih.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
