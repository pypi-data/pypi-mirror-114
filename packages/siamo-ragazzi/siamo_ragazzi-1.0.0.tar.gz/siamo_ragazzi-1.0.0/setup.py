# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['siamo_ragazzi']

package_data = \
{'': ['*'], 'siamo_ragazzi': ['fonts/*']}

install_requires = \
['Pillow>=8.3.1,<9.0.0', 'click>=8.0.1,<9.0.0']

entry_points = \
{'console_scripts': ['siamo-ragazzi = siamo_ragazzi.__main__:main']}

setup_kwargs = {
    'name': 'siamo-ragazzi',
    'version': '1.0.0',
    'description': '"Siamo ragazzi" meme generator',
    'long_description': None,
    'author': 'Stefano Pigozzi',
    'author_email': 'me@steffo.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
