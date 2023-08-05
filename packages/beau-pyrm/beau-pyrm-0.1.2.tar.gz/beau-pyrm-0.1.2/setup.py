# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beau_pyrm']

package_data = \
{'': ['*']}

install_requires = \
['dateparser>=1.0.0,<2.0.0',
 'pandas>=1.3.0,<2.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'rich>=10.6.0,<11.0.0',
 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['beau-pyrm = beau_pyrm.main:app']}

setup_kwargs = {
    'name': 'beau-pyrm',
    'version': '0.1.2',
    'description': 'Very simple relationship manager written in Python.',
    'long_description': '# pyrm\nVery simple relationship manager written in Python.\n',
    'author': 'Beau Hilton',
    'author_email': 'beau.hilton@vumc.org',
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
