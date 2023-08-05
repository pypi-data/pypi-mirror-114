# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['netbox_plugin_unms_import']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'netbox-plugin-unms-import',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Schylar Utley',
    'author_email': 'schylarutley@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
