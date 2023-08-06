# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['et_micc3']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0.0,<8.0.0']

entry_points = \
{'console_scripts': ['micc3 = et_micc3:cli_micc3.main']}

setup_kwargs = {
    'name': 'et-micc3',
    'version': '3.0.0',
    'description': '<Enter a one-sentence description of this project here.>',
    'long_description': '========\net-micc3\n========\n\n\n\n<Enter a one-sentence description of this project here.>\n\n\n* Free software: MIT license\n* Documentation: https://et-micc3.readthedocs.io.\n\n\nFeatures\n--------\n\n* TODO\n',
    'author': 'Bert Tijskens',
    'author_email': 'engelbert.tijskens@uantwerpen.be',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/etijskens/et-micc3',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
