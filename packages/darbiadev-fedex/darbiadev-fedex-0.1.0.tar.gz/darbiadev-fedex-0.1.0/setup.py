# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['darbiadev_fedex', 'darbiadev_fedex.lib']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0', 'xmltodict>=0.12.0,<0.13.0']

extras_require = \
{'docs': ['sphinx>=4.1.1,<5.0.0',
          'sphinx-autodoc-annotation>=1.0-1,<2.0',
          'sphinxcontrib-packages>=1.0.1,<2.0.0',
          'sphinxcontrib-napoleon>=0.7,<0.8',
          'sphinxcontrib-apidoc>=0.3.0,<0.4.0',
          'sphinx-rtd-theme>=0.5.2,<0.6.0',
          'toml>=0.10.2,<0.11.0'],
 'tests': ['pytest>=6.2.4,<7.0.0', 'tox>=3.24.0,<4.0.0']}

setup_kwargs = {
    'name': 'darbiadev-fedex',
    'version': '0.1.0',
    'description': 'darbiadev-fedex',
    'long_description': '# darbiadev-fedex\n',
    'author': 'Bradley Reynolds',
    'author_email': 'bradley.reynolds@darbia.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/darbia/darbiadev-fedex',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
