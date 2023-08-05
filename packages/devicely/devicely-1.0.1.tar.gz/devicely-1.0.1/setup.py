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
    'version': '1.0.1',
    'description': 'Read multiple signals from different sources.',
    'long_description': '[![Actions Status: test](https://github.com/hpi-dhc/devicely/workflows/test/badge.svg)](https://github.com/hpi-dhc/devicely/actions/workflows/test.yml)\n![Coverage Badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/jostmorgenstern/270a0114dfad9251945a146dd6d29fa6/raw/devicely_coverage_main.json)\n[![DOI](https://zenodo.org/badge/279395106.svg)](https://zenodo.org/badge/latestdoi/{279395106})\n[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)\n\n![Devicely Logo](/imgs/logo/devicely-logo.png)\n\ndevicely is a Python package for reading, anonymizing and writing data from various health monitoring sensors.\nWith devicely, you can read sensor data and have it easily accessible in dataframes.\nYou can also anonymize data and write it back using the original data format. This makes it convenient to share health sensor data with other researchers.\n\n[Documentation](https://hpi-dhc.github.io/devicely/)\n\n[PyPi](https://pypi.org/project/devicely/)\n\n## Getting started\n\nTo get started quickly, follow the "Getting started"-section in our docs.\n\nhttps://hpi-dhc.github.io/devicely/\n\n\n## Supported sensors\n\n- [Empatica E4](https://e4.empatica.com/e4-wristband)\n- [Biovotion Everion](https://www.biovotion.com/everion/)\n- [1-lead ECG monitor Faros<sup>TM</sup> 180 from Bittium](https://shop.bittium.com/product/36/bittium-faros-180-solution-pack)\n- [Spacelabs](https://www.spacelabshealthcare.com/products/diagnostic-cardiology/abp-monitoring/90217a/)\n- [Tags (obtained from the app: TimeStamp for Android)](https://play.google.com/store/apps/details?id=gj.timestamp&hl=en)\n- [Shimmer Consensys GSR](https://www.shimmersensing.com/products/gsr-optical-pulse-development-kit#specifications-tab)\n\n## Contributors\n\n```\n* Ariane Sasso\n* Arpita Kappattanavar\n* Bjarne Pfitzner\n* Felix Musmann\n* Jost Morgenstern\n* Lin Zhou\n* Pascal Hecker\n```\n',
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
