# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['perfsizesagemaker',
 'perfsizesagemaker.environment',
 'perfsizesagemaker.load',
 'perfsizesagemaker.reporter',
 'perfsizesagemaker.step']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.17.66,<2.0.0',
 'jinja2>=3.0.1,<4.0.0',
 'perfsize>=0.1.7,<0.2.0',
 'pyyaml>=5.4.1,<6.0.0',
 'yattag>=1.14.0,<2.0.0']

setup_kwargs = {
    'name': 'perfsizesagemaker',
    'version': '0.1.2',
    'description': 'Automated performance testing to determine the right size of infrastructure, applied to AWS SageMaker',
    'long_description': None,
    'author': 'Richard Shiao',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.11,<4.0.0',
}


setup(**setup_kwargs)
