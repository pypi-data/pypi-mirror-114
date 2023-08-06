# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bells', 'bells.commands']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0']

entry_points = \
{'console_scripts': ['bells = bells.__main__:main']}

setup_kwargs = {
    'name': 'bells',
    'version': '0.1.1',
    'description': 'Bells is a program for keeping track of sound recordings.',
    'long_description': '# Bells\n\nBells is a program for keeping track of sound recordings.',
    'author': 'Ceda EI',
    'author_email': 'ceda_ei@webionite.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/ceda_ei/bells.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
