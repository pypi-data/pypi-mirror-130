# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['waffles']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.21.1,<0.22.0', 'python-decouple>=3.5,<4.0', 'rich>=10.15.2,<11.0.0']

setup_kwargs = {
    'name': 'waffles',
    'version': '0.0.4',
    'description': '',
    'long_description': None,
    'author': 'Shahnoza Bekbulaeva',
    'author_email': 'shakhnoza.bekbulaeva@nttdata.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
