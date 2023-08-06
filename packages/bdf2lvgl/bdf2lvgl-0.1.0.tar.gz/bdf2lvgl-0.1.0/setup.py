# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bdf2lvgl', 'bdf2lvgl.codegen']

package_data = \
{'': ['*']}

install_requires = \
['bdflib>=1.1.3,<2.0.0', 'click>=8.0.1,<9.0.0', 'numpy>=1.21.1,<2.0.0']

entry_points = \
{'console_scripts': ['bdf2lvgl = bdf2lvgl.main:main']}

setup_kwargs = {
    'name': 'bdf2lvgl',
    'version': '0.1.0',
    'description': 'Convert bitmap fonts in BDF format to the LVGL font format.',
    'long_description': None,
    'author': 'summivox',
    'author_email': 'summivox@gmail.com',
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
