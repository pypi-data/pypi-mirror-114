# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['perfsize',
 'perfsize.environment',
 'perfsize.load',
 'perfsize.reporter',
 'perfsize.result',
 'perfsize.step']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0', 'numpy>=1.20.3,<2.0.0', 'pandas>=1.2.4,<2.0.0']

setup_kwargs = {
    'name': 'perfsize',
    'version': '0.1.11',
    'description': 'Automated performance testing to determine the right size of infrastructure',
    'long_description': None,
    'author': 'Richard Shiao',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.11,<4.0.0',
}


setup(**setup_kwargs)
