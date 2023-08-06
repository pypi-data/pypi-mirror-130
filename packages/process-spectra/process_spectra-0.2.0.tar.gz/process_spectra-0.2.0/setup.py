# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['process_spectra', 'process_spectra.funcs', 'process_spectra.utils']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.3.2,<4.0.0',
 'numpy>=1.20.0,<2.0.0',
 'pandas>=1.3.4,<2.0.0',
 'scipy>=1.6.2,<2.0.0']

setup_kwargs = {
    'name': 'process-spectra',
    'version': '0.2.0',
    'description': 'A package designed to process optical spectra of fiber optic sensors based on long period gratings (LPGs). The documentation is written in portuguese, since the project was conceived to improve research at a brazilian university lab (LITel - UFJF). If the contents of the library may be useful to you, and you do not speak portuguese, please send us an e-mail.',
    'long_description': None,
    'author': 'Felipe Barino',
    'author_email': 'felipebarino@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/felipebarino/process_spectra',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
