# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['philter_lite', 'philter_lite.filters']

package_data = \
{'': ['*'],
 'philter_lite': ['configs/*',
                  'data/*',
                  'data/i2b2_anno/*',
                  'data/i2b2_notes/*',
                  'data/i2b2_xml/*',
                  'data/phi/*']}

install_requires = \
['chardet>=3.0.4,<4.0.0', 'nltk>=3.5,<4.0', 'xmltodict>=0.12.0,<0.13.0']

entry_points = \
{'console_scripts': ['philter_lite = philter_lite.main:main']}

setup_kwargs = {
    'name': 'philter-lite',
    'version': '0.2.1',
    'description': '',
    'long_description': None,
    'author': 'Beau Norgeot',
    'author_email': 'beaunorgeot@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
