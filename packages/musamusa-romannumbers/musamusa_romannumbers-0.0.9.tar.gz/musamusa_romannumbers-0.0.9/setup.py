# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['musamusa_romannumbers']

package_data = \
{'': ['*']}

install_requires = \
['musamusa-errors>=0.9.1,<0.10.0']

setup_kwargs = {
    'name': 'musamusa-romannumbers',
    'version': '0.0.9',
    'description': 'Roman Numbers (XVI <-> 16)',
    'long_description': None,
    'author': 'suizokukan',
    'author_email': 'suizokukan@orange.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
