# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['axiom']

package_data = \
{'': ['*']}

install_requires = \
['dacite>=1.6.0,<2.0.0',
 'pyhumps>=1.6.1,<2.0.0',
 'requests-toolbelt>=0.9.1,<0.10.0',
 'requests>=2.25.1,<3.0.0',
 'ujson>=4.0.2,<5.0.0']

setup_kwargs = {
    'name': 'axiom-py',
    'version': '0.1.0b2',
    'description': 'Axiom API Python bindings.',
    'long_description': None,
    'author': 'Axiom, Inc.',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
