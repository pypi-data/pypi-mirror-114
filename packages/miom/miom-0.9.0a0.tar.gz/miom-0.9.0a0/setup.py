# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['miom']

package_data = \
{'': ['*']}

install_requires = \
['gurobipy>=9.1.2,<10.0.0',
 'mip>=1.13.0,<2.0.0',
 'mosek>=9.2.47,<10.0.0',
 'numpy>=1.20.3,<2.0.0',
 'picos>=2.2.43,<3.0.0',
 'swiglpk>=5.0.3,<6.0.0']

setup_kwargs = {
    'name': 'miom',
    'version': '0.9.0a0',
    'description': 'Mixed Integer Optimization for Metabolism',
    'long_description': None,
    'author': 'Pablo R. Mier',
    'author_email': 'pablo.rodriguez.mier@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
