# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sloth_ci', 'sloth_ci_ext_api', 'sloth_ci_ext_db']

package_data = \
{'': ['*']}

install_requires = \
['CherryPy>=18.6.0,<19.0.0',
 'PyYAML>=5.4.1,<6.0.0',
 'Routes>=2.5.1,<3.0.0',
 'cliar>=1.3.4,<2.0.0',
 'requests>=2.26.0,<3.0.0',
 'tabulate>=0.8.9,<0.9.0']

extras_require = \
{'colored_logs': ['colorama[colored_logs]>=0.4.4,<0.5.0']}

entry_points = \
{'console_scripts': ['sci = sloth_ci.cli:main', 'sloth-ci = sloth_ci.cli:main']}

setup_kwargs = {
    'name': 'sloth-ci',
    'version': '2.2.0',
    'description': 'Lightweight, standalone CI server.',
    'long_description': '# Welcome to Sloth CI!\n\n[![image](https://img.shields.io/pypi/v/sloth-ci.svg)](https://pypi.org/project/sloth-ci)\n[![Build Status](https://travis-ci.com/Sloth-CI/sloth-ci.svg?branch=develop)](https://travis-ci.com/Sloth-CI/sloth-ci)\n\n\n**Sloth CI** is a lightweight, standalone CI server.\n\nVia extensions, Sloth CI offers detailed logs, build status badges, email notifications, and webhooks. \n\n\n## Run Locally\n\nDeploy the project with Poetry:\n\n    $ poetry install\n\nRun locally with:\n\n    $ poetry run sci start\n\nCheck that the instance is running:\n\n    $ poetry run sci status\n\nBuild the docs:\n\n    $ poetry run foliant make site -p docs\n',
    'author': 'Constantine Molchanov',
    'author_email': 'moigagoo@live.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sloth-ci/sloth-ci/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
