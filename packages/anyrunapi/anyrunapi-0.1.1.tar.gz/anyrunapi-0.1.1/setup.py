# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['anyrunapi']

package_data = \
{'': ['*']}

install_requires = \
['argparse>=1.4.0,<2.0.0', 'coloredlogs>=15.0,<16.0', 'requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['anyrun = anyrunapi.cli:main']}

setup_kwargs = {
    'name': 'anyrunapi',
    'version': '0.1.1',
    'description': 'Library and CLI tool for Any Run (any.run) malware sandbox api.',
    'long_description': None,
    'author': 'Sean McFeely',
    'author_email': 'mcfeelynaes@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
