# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tfdevops']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.18.16,<2.0.0',
 'click>=8.0.1,<9.0.0',
 'jmespath>=0.10.0,<0.11.0',
 'jsonschema>=3.2.0,<4.0.0']

entry_points = \
{'console_scripts': ['tfdevops = tfdevops.cli:cli']}

setup_kwargs = {
    'name': 'tfdevops',
    'version': '0.1.0',
    'description': 'Terraform Support for AWS DevOps Guru',
    'long_description': None,
    'author': 'Kapil Thangavelu',
    'author_email': 'kapilt@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
