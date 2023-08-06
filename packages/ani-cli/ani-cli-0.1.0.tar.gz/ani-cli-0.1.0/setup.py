# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ani-cli']

package_data = \
{'': ['*']}

install_requires = \
['InquirerPy>=0.3.0,<0.4.0', 'requests>=2.26.0,<3.0.0']

entry_points = \
{'console_scripts': ['ani = main:main']}

setup_kwargs = {
    'name': 'ani-cli',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'sleepntsheep',
    'author_email': 'sheep@papangkorn.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
