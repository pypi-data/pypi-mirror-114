# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openfabric_pysdk']

package_data = \
{'': ['*']}

install_requires = \
['Flask-RESTful>=0.3.9,<0.4.0',
 'Flask>=1.1.2,<1.2.0',
 'apispec>=4.4.0,<4.5.0',
 'connexion>=2.9.0,<3.0.0',
 'flask-apispec>=0.11.0,<0.12.0',
 'marshmallow>=3.11.1,<3.12.0']

setup_kwargs = {
    'name': 'openfabric-pysdk',
    'version': '0.1.2',
    'description': 'Openfabric Python SDK',
    'long_description': '',
    'author': 'Andrei Tara',
    'author_email': 'andrei@openfabric.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://openfabric.ai',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
