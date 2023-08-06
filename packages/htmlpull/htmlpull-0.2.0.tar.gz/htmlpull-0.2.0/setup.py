# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['htmlpull']

package_data = \
{'': ['*']}

install_requires = \
['docopt>=0.6.2,<0.7.0', 'html5lib>=1.1,<2.0', 'lxml>=4.6.4,<5.0.0']

entry_points = \
{'console_scripts': ['htmlpull = htmlpull.cli:cli']}

setup_kwargs = {
    'name': 'htmlpull',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Summer',
    'author_email': '30243134+Summertime@users.noreply.github.com',
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
