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
    'version': '0.1.2',
    'description': 'Manage your Makefiles from python',
    'long_description': "# pymakefile\nManage your Makefiles with python\n\n## Install\n```\npip install pymakefile\n```\n## Usage\n\n### Starting a new Makefile\n```console\npymake init\n```\n\n### Add a new command to the Makefile\n```\npymake add '{command_name}' '{command}' '{description}'\n```  \n\nExample of adding new command:  \n```\npymake add runlocal 'python manage.py runserver' 'Starts the development server'\n```\n\n### Show available commands in Makefile\n```\nmake help\n```\n\n## Development\n### Install dependencies\n```\npoetry install\n```\n### Activate virtualenv\n```\npoetry shell\n```\n### Running the commands from source\n```\npython pymakefile.py init\n```\n```\npython pymakefile.py add '{command_name}' '{command}' '{description}'\n```\n\n### Applying lint rules\n```\nblack .\n```\n",
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
