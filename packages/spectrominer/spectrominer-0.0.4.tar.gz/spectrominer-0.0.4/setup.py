# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spectrominer',
 'spectrominer.corrections',
 'spectrominer.parser',
 'spectrominer.ui']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.4.1,<4.0.0',
 'openpyxl>=3.0.7,<4.0.0',
 'pandas>=1.2.3,<2.0.0',
 'xlrd>=2.0.1,<3.0.0']

entry_points = \
{'console_scripts': ['spectrominer = spectrominer.ui.app:start']}

setup_kwargs = {
    'name': 'spectrominer',
    'version': '0.0.4',
    'description': 'Spectrominer is a software that allows you to apply corrections to mass spectrometry data.',
    'long_description': '# SpectroMiner\nSpectrominer is a software that allows you to apply corrections to mass spectrometry data.\nMore precisely, it uses control measures in order to subtract the natural presence of isotopes.\n\nProject Status: in development\n\n## Installation\n### Windows\nsee the [releases](https://github.com/ulaval-rs/spectrominer/releases)\n\nTo run spectrominer, run the .exe.\n\n### Macos\n#### From the release\nsee the [releases](https://github.com/ulaval-rs/spectrominer/releases)\n\n#### From PyPi\nInstallation through PyPi is also possible.\nBe sure [brew](https://brew.sh/) is installed,\nand from the terminal:\n```bash\n$ brew install python3\n$ brew install python-tk\n```\nAnd then:\n```bash\n$ pip install spectrominer\n```\n\n### PyPi\nTo install:\n```bash\n$ pip install spectrominer\n```\nTo run spectrominer:\n```bash\n$ spectrominer\n```\nor\n```bash\n$ /path/to/python/bin/spectrominer\n```\n',
    'author': 'Gabriel Couture',
    'author_email': 'gacou54@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ulaval-rs/spectrominer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
