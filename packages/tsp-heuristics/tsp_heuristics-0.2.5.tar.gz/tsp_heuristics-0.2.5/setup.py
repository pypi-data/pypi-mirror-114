# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tsp_heuristics', 'tsp_heuristics.heuristics', 'tsp_heuristics.utils']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.4.2,<4.0.0',
 'numpy>=1.21.1,<2.0.0',
 'pandas>=1.3.0,<2.0.0',
 'sympy>=1.8,<2.0',
 'tsplib95>=0.7.1,<0.8.0']

setup_kwargs = {
    'name': 'tsp-heuristics',
    'version': '0.2.5',
    'description': 'Meta-heuristics for solving the TSP',
    'long_description': None,
    'author': 'Adriel Martins',
    'author_email': 'adrielfalcao@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
