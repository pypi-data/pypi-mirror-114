# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymakefile']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0']

entry_points = \
{'console_scripts': ['pymake = pymakefile.pymakefile:main']}

setup_kwargs = {
    'name': 'pymakefile',
    'version': '0.1.1',
    'description': 'Manage your Makefiles from python',
    'long_description': "# pymakefile\nManage your Makefiles from python\n\n## Install\n\n## Usage\n\n### Starting a new Makefile\n`pymake init`\n\n### Add a new command to the Makefile\n`pymake add '{command_name}' '{command}' '{description}'`  \nExample:  \n`pymake add runlocal 'python manage.py runserver' 'Starts the development server'`\n\n## Development\n### Install dependencies\n`poetry install`\n### Activate virtualenv\n`poetry shell`\n### Running the commands from source\n- `python pymakefile.py init`\n- `python pymakefile.py add '{command_name}' '{command}' '{description}'`\n\n### Applying lint rules\n`black .`\n",
    'author': 'William',
    'author_email': 'macwilliamdlc@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/willbackslash/pymakefile',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
