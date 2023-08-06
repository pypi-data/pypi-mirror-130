# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['music_organizer']

package_data = \
{'': ['*']}

install_requires = \
['audio-metadata>=0.11.1,<0.12.0', 'typer>=0.4.0,<0.5.0']

setup_kwargs = {
    'name': 'music-organizer',
    'version': '0.1.1',
    'description': 'Music files organizer',
    'long_description': None,
    'author': 'JOramas',
    'author_email': 'javiale2000@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
