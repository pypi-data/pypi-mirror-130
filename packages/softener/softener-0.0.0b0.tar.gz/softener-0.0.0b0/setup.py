# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['softener', 'softener.cli', 'softener.cli.cmds', 'softener.core']

package_data = \
{'': ['*'], 'softener': ['data/schemas/*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'charset-normalizer>=2.0.7,<3.0.0',
 'click>=8.0.3,<9.0.0',
 'inflection>=0.5.1,<0.6.0',
 'lxml>=4.6.4,<5.0.0',
 'pastel>=0.2.1,<0.3.0',
 'pyjq>=2.5.2,<3.0.0',
 'sh>=1.14.2,<2.0.0',
 'wrapt>=1.13.3,<2.0.0']

entry_points = \
{'console_scripts': ['softener = softener.cli.cmds:main']}

setup_kwargs = {
    'name': 'softener',
    'version': '0.0.0b0',
    'description': 'A CLI tool for generating GitHub workflow annotations',
    'long_description': '# Softener\n\n_A CLI tool for GitHub Actions that can generate annotations directly from the\noutput of your workflows_\n\n> 🚧&nbsp;&nbsp;**This repository is under construction**\n',
    'author': 'norosa',
    'author_email': '23469+norosa@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bottle-garden/softener',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
