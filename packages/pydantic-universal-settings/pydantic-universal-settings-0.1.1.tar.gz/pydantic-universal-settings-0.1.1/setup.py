# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydantic_universal_settings']

package_data = \
{'': ['*']}

install_requires = \
['click-option-group>=0.5.3,<0.6.0',
 'psutil>=5.8.0,<6.0.0',
 'pydantic[dotenv]>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'pydantic-universal-settings',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'tc-imba',
    'author_email': 'liuyh970615@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
