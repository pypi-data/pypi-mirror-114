# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['skb']

package_data = \
{'': ['*']}

install_requires = \
['lxml>=4.6.3,<5.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0']}

entry_points = \
{'console_scripts': ['skb = skb.skb:main']}

setup_kwargs = {
    'name': 'skb',
    'version': '1.2.7',
    'description': 'Synth Kit builder for Synthstrom Deluge',
    'long_description': None,
    'author': 'neilbaldwin',
    'author_email': 'neil.baldwin@mac.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
