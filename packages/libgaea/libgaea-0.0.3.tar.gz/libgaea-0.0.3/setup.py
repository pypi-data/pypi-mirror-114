# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gaea']

package_data = \
{'': ['*']}

install_requires = \
['PySide6>=6.1.2,<7.0.0', 'sh>=1.14.2,<2.0.0']

setup_kwargs = {
    'name': 'libgaea',
    'version': '0.0.3',
    'description': 'Spawner of the understory',
    'long_description': '# gaea\nSpawn and manage your personal websites\n\nDownload and run the most recent [release](https://github.com/canopy/gaea/releases)\nfor your operating system.\n',
    'author': 'Angelo Gladding',
    'author_email': 'self@angelogladding.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
