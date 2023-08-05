# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['elbat']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.22,<2.0.0',
 'cx-Oracle>=8.2.1,<9.0.0',
 'loguru>=0.5.3,<0.6.0',
 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['elbat = elbat.main:app', 'gluent = elbat.main:app']}

setup_kwargs = {
    'name': 'elbat',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Cody Fincher',
    'author_email': 'cody@gluent.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
