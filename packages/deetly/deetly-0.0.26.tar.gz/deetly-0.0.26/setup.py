# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['deetly']

package_data = \
{'': ['*']}

install_requires = \
['isodate>=0.6.0,<0.7.0',
 'pandas>=1.1.4,<2.0.0',
 'plotly',
 'python-dateutil>=2.8.1,<3.0.0',
 'requests>=2.20.0,<3.0.0',
 'schema>=0.7.4,<0.8.0',
 'urllib3>=1.26.0,<2.0.0']

setup_kwargs = {
    'name': 'deetly',
    'version': '0.0.26',
    'description': 'toolkit for creating data packages',
    'long_description': None,
    'author': 'Paul Bencze',
    'author_email': 'paul@idelab.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.8,<4.0.0',
}


setup(**setup_kwargs)
