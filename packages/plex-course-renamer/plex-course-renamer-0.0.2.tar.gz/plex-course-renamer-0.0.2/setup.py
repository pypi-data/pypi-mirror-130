# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['plex_course_renamer']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0']

entry_points = \
{'console_scripts': ['rename = plex_course_renamer.rename:run']}

setup_kwargs = {
    'name': 'plex-course-renamer',
    'version': '0.0.2',
    'description': '',
    'long_description': None,
    'author': 'Eric Warren',
    'author_email': 'ericwarren99@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
