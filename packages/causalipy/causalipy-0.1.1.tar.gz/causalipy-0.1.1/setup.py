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
    'version': '0.1.1',
    'description': 'Causal Methods Implemented in Python',
    'long_description': '# CausaliPy\n\nCausal Methods implemented in Python.\n\n## Installation\n\nInstall via\n\n```\npip install causalipy\n```\n\nIt might make sense to add the py-arrow dependency (which is currently required\nfor the example):\n\n```\npip install pyarrow\n```\n\n## Example\n\nTo run a version of the multi-period difference-in-difference estimator as\nproposed by Callaway and Sant’Anna (2020)  (this requires additionally pyarrow  - e.g. via\n`pip install pyarrow` - to be installed currently):\n\n```python\nfrom causalipy.did.multi_periods import MultiPeriodDid\nimport pandas as pd\n\nurl = "https://github.com/mohelm/causalipy-datasets/raw/main/mpdta-sample.feather"\ndata = pd.read_feather(url)\n\nmpd_minimum_wage = MultiPeriodDid(\n    data,\n    outcome="lemp",\n    treatment_indicator="treat",\n    time_period_indicator="year",\n    group_indiciator="first.treat",\n    formula="~ 1",\n)\nmpd_minimum_wage.plot_treatment_effects()\n```\n\nThis will give:\n\n![alt text](./readme_fig.png)\n\n## License\n\nThis project is licensed under the terms of the MIT license.\n\n',
    'author': 'Moritz Helm',
    'author_email': 'mohelm84@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mohelm/causalipy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
