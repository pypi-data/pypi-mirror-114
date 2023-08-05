# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['devicely']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.21.1,<2.0.0', 'pandas>=1.3.0,<2.0.0', 'pyEDFlib>=0.1.22,<0.2.0']

setup_kwargs = {
    'name': 'devicely',
    'version': '1.0.0',
    'description': 'Read multiple signals from different sources.',
    'long_description': None,
    'author': 'Ariane Morassi Sasso',
    'author_email': 'ariane.morassi-sasso@hpi.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hpi-dhc/devicely',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
