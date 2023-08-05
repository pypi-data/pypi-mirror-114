# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sfu_data_io']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.12,<2.0', 'numpy', 's3fs>=0.6,<0.7']

setup_kwargs = {
    'name': 'sfu-data-io',
    'version': '0.1.1',
    'description': 'A set of helpers that transfer data across different filesystems.',
    'long_description': None,
    'author': 'Anderson de Andrade',
    'author_email': 'adeandrade@ensc.sfu.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
