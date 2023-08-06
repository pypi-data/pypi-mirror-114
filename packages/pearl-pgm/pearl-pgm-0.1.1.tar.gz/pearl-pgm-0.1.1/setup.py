# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pearl', 'pearl.nodes', 'pearl.structure']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'h5py>=3.2.1,<4.0.0',
 'networkx>=2.4,<3.0',
 'numpy>=1.20.3,<2.0.0',
 'pyro-ppl>=1.4.0,<2.0.0',
 'torch>=1.6.0,<2.0.0']

setup_kwargs = {
    'name': 'pearl-pgm',
    'version': '0.1.1',
    'description': 'Library for declarative specification of directed graphical models and inference using Pyro.',
    'long_description': '# pearl-pgm\n\nLibrary for declarative specification of directed graphical models and inference using Pyro.\n',
    'author': 'Arun Nampally',
    'author_email': 'arun.nampally@invitae.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/invitae/pearl-pgm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
