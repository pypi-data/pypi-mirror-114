# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tests', 'xepmts_endpoints', 'xepmts_endpoints.endpoint_templates']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0', 'click']

entry_points = \
{'console_scripts': ['xepmts_endpoints = xepmts_endpoints.cli:main']}

setup_kwargs = {
    'name': 'xepmts-endpoints',
    'version': '0.1.3',
    'description': 'Top-level package for xepmts-endpoints.',
    'long_description': '================\nxepmts-endpoints\n================\n\n\n.. image:: https://img.shields.io/pypi/v/xepmts_endpoints.svg\n        :target: https://pypi.python.org/pypi/xepmts_endpoints\n\n.. image:: https://img.shields.io/travis/jmosbacher/xepmts_endpoints.svg\n        :target: https://travis-ci.com/jmosbacher/xepmts_endpoints\n\n.. image:: https://readthedocs.org/projects/xepmts-endpoints/badge/?version=latest\n        :target: https://xepmts-endpoints.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n\n\n\n\nEndpoint definitions for xepmts api\n\n\n* Free software: MIT\n* Documentation: https://xepmts-endpoints.readthedocs.io.\n\n\nFeatures\n--------\n\n* TODO\n\nCredits\n-------\n\nThis package was created with Cookiecutter_ and the `briggySmalls/cookiecutter-pypackage`_ project template.\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`briggySmalls/cookiecutter-pypackage`: https://github.com/briggySmalls/cookiecutter-pypackage\n',
    'author': 'Yossi Mosbacher',
    'author_email': 'joe.mosbacher@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jmosbacher/xepmts_endpoints',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
