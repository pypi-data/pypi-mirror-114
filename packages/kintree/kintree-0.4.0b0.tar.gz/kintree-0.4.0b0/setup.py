# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kintree',
 'kintree.common',
 'kintree.config',
 'kintree.database',
 'kintree.kicad',
 'kintree.search',
 'kintree.wrapt_timeout_decorator']

package_data = \
{'': ['*'],
 'kintree.config': ['digikey/*', 'inventree/*', 'kicad/*', 'settings/*'],
 'kintree.kicad': ['templates/*', 'templates_project/*']}

install_requires = \
['PySimpleGUI>=4.28.0,<5.0',
 'PyYAML>=5.3.1,<6.0',
 'digikey-api>=0.4.0,<1.0',
 'fuzzywuzzy>=0.18.0,<1.0',
 'inventree>=0.2.4,<1.0',
 'multiprocess>=0.70.12.2,<0.71',
 'python-Levenshtein>=0.12.2,<0.13.0',
 'validators>=0.18.2',
 'wrapt>=1.12.1,<2.0']

entry_points = \
{'console_scripts': ['kintree = kintree:kintree_gui.main',
                     'kintree_setup_inventree = kintree:setup_inventree.main']}

setup_kwargs = {
    'name': 'kintree',
    'version': '0.4.0b0',
    'description': 'Fast part creation in KiCad and InvenTree',
    'long_description': None,
    'author': 'Placeholder Name',
    'author_email': 'placeholder@test.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
