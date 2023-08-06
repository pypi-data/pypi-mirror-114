# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['D47calib']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'd47calib',
    'version': '0.0.4',
    'description': 'D47calib library',
    'long_description': None,
    'author': 'Mathieu Daëron',
    'author_email': 'mathieu@daeron.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
