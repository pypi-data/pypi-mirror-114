# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['elemental']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23,<3.0', 'xmltodict>=0.12.0,<0.13.0']

setup_kwargs = {
    'name': 'python-elemental',
    'version': '0.7.3',
    'description': 'Python Client for Elemental On-Premises Appliances',
    'long_description': '\n# Elemental\n\n[![continuous integration status](https://github.com/cbsinteractive/elemental/workflows/CI/badge.svg)](https://github.com/cbsinteractive/elemental/actions?query=workflow%3ACI)\n[![codecov](https://codecov.io/gh/cbsinteractive/elemental/branch/master/graph/badge.svg?token=qFdUKsI2tD)](https://codecov.io/gh/cbsinteractive/elemental)\n\n\nPython Client for Elemental On-Premises Appliances\n\n## Run Tests\n\nBefore running tests locally, install `tox` and `poetry`.\n\n    pipx install tox\n    pipx install poetry\n\nRun tests using\n\n    make test\n\nTo run lint, use\n\n    make lint\n\n## Release Updated Version\nUse the Github UI to [create a new release](https://github.com/cbsinteractive/elemental/releases/new), the tag needs\nto follow the semver format `0.0.0`. After the new release is created, a Github workflow will build and publish the\nnew python package to PyPI automatically.\n',
    'author': 'CBS Interactive',
    'author_email': 'video-processing-team@cbsinteractive.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cbsinteractive/elemental.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
