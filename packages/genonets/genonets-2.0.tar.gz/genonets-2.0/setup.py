# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['genonets', 'genonets.sample']

package_data = \
{'': ['*'], 'genonets.sample': ['data/*']}

install_requires = \
['numpy>=1.19,<2.0', 'python-igraph==0.8.2', 'tqdm>=4.49.0,<5.0.0']

setup_kwargs = {
    'name': 'genonets',
    'version': '2.0',
    'description': 'Framework for creating and analyzing genotype networks from.',
    'long_description': '# Genonets\n\nWelcome to the latest version of Genonets. The project now uses Python 3.8+, \nwith several feature and performance upgrades. A previous version based on \nPython 2 was used as the backend for the \n[Genonets Server](#Genonets-Server-end-of-life).\n\n## Documentation\n\nInstallation and usage instructions, as well as further documentation is \navailable [here](https://genonets.readthedocs.io/).\n\n## Genonets Server end-of-life\n\nThe Genonets Server had to be shut down due to lack of funding for web hosting \nservices. Nevertheless, all analyses are still available in the Genonets \npackage via this repository.\n\n## Contact\n\n**Note:** Please [email us](mailto:genonets@outlook.com) for any questions \nand/or comments.\n',
    'author': 'Fahad Khalid',
    'author_email': 'genonets@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fkhalid/genonets',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
