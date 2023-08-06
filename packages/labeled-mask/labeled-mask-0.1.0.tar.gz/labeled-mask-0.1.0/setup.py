# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['labeled_mask']

package_data = \
{'': ['*']}

extras_require = \
{':python_version >= "2.7.0" and python_version < "2.8.0"': ['numpy>=1.16,<2.0']}

setup_kwargs = {
    'name': 'labeled-mask',
    'version': '0.1.0',
    'description': 'Provide interface of tagged mask that make easy to squeeze target data from array',
    'long_description': None,
    'author': 'wwwshwww',
    'author_email': 'www.shinderu.www@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=2.7',
}


setup(**setup_kwargs)
