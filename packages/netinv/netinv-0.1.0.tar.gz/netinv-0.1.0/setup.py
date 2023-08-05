# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['netinv']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1,<2']

setup_kwargs = {
    'name': 'netinv',
    'version': '0.1.0',
    'description': 'Network inventory with async connection support',
    'long_description': '## NetInv — network inventory with async connection support\nInspired by [nornir](https://github.com/nornir-automation/nornir)\n\nSupported on Python 3.6.2+',
    'author': 'Dmitry Figol',
    'author_email': 'git@dmfigol.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dmfigol/netinv',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
