# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tap_krow', 'tap_krow.tests']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0', 'singer-sdk>=0.3.15,<0.4.0']

entry_points = \
{'console_scripts': ['tap-krow = tap_krow.tap:TapKrow.cli']}

setup_kwargs = {
    'name': 'tap-krow',
    'version': '0.2.0',
    'description': '`tap-krow` is a Singer tap for the KROW API, built with the Meltano SDK for Singer Taps.',
    'long_description': None,
    'author': 'Datateer',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<3.10',
}


setup(**setup_kwargs)
