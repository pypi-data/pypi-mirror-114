# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['elbat', 'elbat.commands', 'elbat.workflows']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.22,<2.0.0',
 'click-help-colors>=0.9.1,<0.10.0',
 'cx-Oracle>=8.2.1,<9.0.0',
 'loguru>=0.5.3,<0.6.0',
 'typer[all]>=0.3.2,<0.4.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0']}

entry_points = \
{'console_scripts': ['elbat = elbat.main:main', 'gluent = elbat.main:main']}

setup_kwargs = {
    'name': 'elbat',
    'version': '0.1.1',
    'description': '',
    'long_description': 'None',
    'author': 'Cody Fincher',
    'author_email': 'cody@gluent.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
