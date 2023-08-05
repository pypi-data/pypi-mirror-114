# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mananeras', 'mananeras.dataset']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0',
 'click>=7,<8',
 'dateparser>=1.0.0,<2.0.0',
 'html5lib>=1.1,<2.0',
 'kaggle>=1.5.12,<2.0.0',
 'lxml>=4.6.3,<5.0.0',
 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'mananeras',
    'version': '0.1.4',
    'description': 'Las conferencias mananeras del presidente de México',
    'long_description': None,
    'author': 'Antonio Feregrino',
    'author_email': 'antonio.feregrino@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
