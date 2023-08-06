# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysesame3', 'tests']

package_data = \
{'': ['*'], 'tests': ['fixtures/*']}

install_requires = \
['pycryptodome>=3.10.1,<4.0.0', 'requests>=2.25.1,<3.0.0']

extras_require = \
{':python_version < "3.8"': ['typing-extensions>=3.10.0.0,<4.0.0.0',
                             'importlib-metadata>=4.6,<5.0'],
 'cognito': ['awsiotsdk>=1.6.1,<2.0.0',
             'boto3>=1.17.94,<2.0.0',
             'certifi',
             'requests-aws4auth>=1.1.1,<2.0.0'],
 'doc': ['livereload>=2.6.3,<3.0.0',
         'mkdocs>=1.1.2,<2.0.0',
         'mkdocstrings>=0.15.0,<0.16.0',
         'mkdocs-autorefs>=0.2.1,<0.3.0',
         'mkdocs-include-markdown-plugin>=3.1.3,<4.0.0',
         'mkdocs-material>=7.1.8,<8.0.0']}

setup_kwargs = {
    'name': 'pysesame3',
    'version': '0.5.0rc2',
    'description': 'Unofficial library to communicate with Sesame smart locks.',
    'long_description': '# pysesame3\n\n_Unofficial Python Library to communicate with SESAME 3 series products from CANDY HOUSE, Inc._\n\n[![PyPI](https://img.shields.io/pypi/v/pysesame3)](https://pypi.python.org/pypi/pysesame3)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pysesame3)\n![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/mochipon/pysesame3/dev%20workflow/main)\n[![Documentation Status](https://readthedocs.org/projects/pysesame3/badge/?version=latest)](https://pysesame3.readthedocs.io/en/latest/?badge=latest)\n[![codecov](https://codecov.io/gh/mochipon/pysesame3/branch/main/graph/badge.svg?token=2Y7OPZTILT)](https://codecov.io/gh/mochipon/pysesame3)\n![PyPI - License](https://img.shields.io/pypi/l/pysesame3)\n\nThis project aims to control SESAME 3 series devices by using **[the cloud service](https://doc.candyhouse.co/ja/flow_charts#candy-house-cloud-%E3%81%A8-wifi-module-%E7%B5%8C%E7%94%B1%E3%81%A7-sesame-%E3%82%92%E9%81%A0%E9%9A%94%E6%93%8D%E4%BD%9C)**.\nIf you want to control them directly via **Bluetooth connection**, please check [pysesameos2](https://github.com/mochipon/pysesameos2).\n\n* Free software: MIT license\n* Documentation: [https://pysesame3.readthedocs.io](https://pysesame3.readthedocs.io)\n\n## Supported devices\n\n- [SESAME 3](https://jp.candyhouse.co/products/sesame3)\n- [SESAME bot](https://jp.candyhouse.co/products/sesame3-bot)\n\n## Features\n\n* Retrieve the device status (battery level, locked, handle position, etc.).\n* Retrieve recent events (locked, unlocked, etc.) associated with a lock.\n* Needless to say, locking, unlocking and clicking (for the bot)!\n\n## Usage\n\nPlease take a look at [the documentation](https://pysesame3.readthedocs.io/en/latest/usage/).\n\n## Credits & Thanks\n\n* A huge thank you to all at [CANDY HOUSE](https://jp.candyhouse.co/) and their crowdfunding contributors!\n* Thanks to [@Chabiichi](https://github.com/Chabiichi)-san for [the offer](https://github.com/mochipon/pysesame3/issues/25) to get my SESAME bot!\n* This project was inspired and based on [tchellomello/python-ring-doorbell](https://github.com/tchellomello/python-ring-doorbell) and [snjoetw/py-august](https://github.com/snjoetw/py-august).\n',
    'author': 'Masaki Tagawa',
    'author_email': 'masaki@tagawa.email',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mochipon/pysesame3',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
