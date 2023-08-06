# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pcmf']

package_data = \
{'': ['*']}

install_requires = \
['tensorflow>=2.5.0,<3.0.0']

setup_kwargs = {
    'name': 'pcmf',
    'version': '0.1.0',
    'description': 'PCMF is a Python package of Positive Collective Matrix Factorization(PCMF). PCMF is a model that combines the interpretability of NMF and the extensibility of CMF.',
    'long_description': None,
    'author': 'Y. Sumiya',
    'author_email': 'y.sumiya.1031@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<3.9',
}


setup(**setup_kwargs)
