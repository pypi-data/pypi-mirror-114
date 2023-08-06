# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['px4ctl', 'px4ctl.platforms']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=21.0.0,<22.0.0',
 'cattrs>=1.7.1,<2.0.0',
 'click>=8.0,<9.0',
 'dronekit>=2.9.2,<3.0.0',
 'mavsdk>=0.17.0,<0.18.0']

extras_require = \
{'docs': ['Sphinx>=3.5.4,<4.0.0',
          'sphinx-autodocgen>=1.2,<2.0',
          'sphinx-rtd-theme>=0.5.2,<0.6.0']}

entry_points = \
{'console_scripts': ['px4ctl = px4ctl.__main__:px4ctl']}

setup_kwargs = {
    'name': 'px4ctl',
    'version': '1.0.0a6',
    'description': 'Command-line mission planning, execution and monitoring for MAVSDK',
    'long_description': None,
    'author': 'Quinn Thibeault',
    'author_email': 'quinn.thibeault96@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
