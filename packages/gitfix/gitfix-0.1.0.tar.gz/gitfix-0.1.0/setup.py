# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gitfix']

package_data = \
{'': ['*']}

install_requires = \
['blessed', 'rich>=10.6.0,<11.0.0']

entry_points = \
{'console_scripts': ['gitfix = gitfix.main:main']}

setup_kwargs = {
    'name': 'gitfix',
    'version': '0.1.0',
    'description': 'Command-line tool to help you recover from a broken git state.',
    'long_description': None,
    'author': 'Lucas Melin',
    'author_email': 'lucas.melin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
