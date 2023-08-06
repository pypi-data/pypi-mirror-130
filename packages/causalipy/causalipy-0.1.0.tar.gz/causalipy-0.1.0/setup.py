# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['causalipy', 'causalipy.did']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.0,<4.0.0',
 'pandas>=1.3.4,<2.0.0',
 'patsy>=0.5.2,<0.6.0',
 'scipy>=1.7.2,<2.0.0']

setup_kwargs = {
    'name': 'causalipy',
    'version': '0.1.0',
    'description': 'Econometrics for Python',
    'long_description': None,
    'author': 'Moritz Helm',
    'author_email': 'mohelm84@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
