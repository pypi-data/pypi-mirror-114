# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['avilla',
 'avilla.builtins',
 'avilla.event',
 'avilla.execution',
 'avilla.message',
 'avilla.network',
 'avilla.network.clients',
 'avilla.network.services',
 'avilla.onebot',
 'avilla.tools',
 'avilla.tools.kanata',
 'avilla.tools.literature',
 'avilla.utilles']

package_data = \
{'': ['*']}

modules = \
['py']
install_requires = \
['aiofiles>=0.7.0,<0.8.0',
 'aiohttp>=3.7.4,<4.0.0',
 'graia-broadcast>=0.11.3,<0.12.0',
 'immutables>=0.15,<0.16',
 'pydantic>=1.8.2,<2.0.0',
 'yarl>=1.6.3,<2.0.0']

setup_kwargs = {
    'name': 'avilla-core',
    'version': '0.0.2',
    'description': '',
    'long_description': None,
    'author': 'GreyElaina',
    'author_email': 'GreyElaina@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
