# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['conntask_ni']

package_data = \
{'': ['*'], 'conntask_ni': ['files/*']}

install_requires = \
['nibabel>=3.2.1,<4.0.0',
 'numpy>=1.21.1,<2.0.0',
 'pandas>=1.3.0,<2.0.0',
 'scikit-learn>=0.24.2,<0.25.0',
 'scipy>=1.7.0,<2.0.0']

setup_kwargs = {
    'name': 'conntask-ni',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'shachar_gal',
    'author_email': 'gal.shachar@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
