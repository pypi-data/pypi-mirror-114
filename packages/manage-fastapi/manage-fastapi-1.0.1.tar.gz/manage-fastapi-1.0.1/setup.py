# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['manage_fastapi',
 'manage_fastapi.templates',
 'manage_fastapi.templates.app',
 'manage_fastapi.templates.app.hooks',
 'manage_fastapi.templates.app.{{ cookiecutter.folder_name }}',
 'manage_fastapi.templates.app.{{ cookiecutter.folder_name }}.api',
 'manage_fastapi.templates.project',
 'manage_fastapi.templates.project.hooks',
 'manage_fastapi.templates.project.{{ cookiecutter.folder_name }}.app',
 'manage_fastapi.templates.project.{{ cookiecutter.folder_name }}.app.core',
 'manage_fastapi.templates.project.{{ cookiecutter.folder_name }}.tests']

package_data = \
{'': ['*'],
 'manage_fastapi.templates.project': ['{{ cookiecutter.folder_name }}/*']}

install_requires = \
['bullet>=2.2.0,<3.0.0',
 'cookiecutter>=1.7.2,<2.0.0',
 'pydantic[email]>=1.7.2,<2.0.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['fastapi = manage_fastapi.main:app']}

setup_kwargs = {
    'name': 'manage-fastapi',
    'version': '1.0.1',
    'description': 'Managing FastAPI projects made easy.',
    'long_description': '<div align="center">\n<h1>manage-fastapi</h1>\n\n[manage-fastapi](https://github.com/ycd/manage-fastapi) Project generator and manager for FastAPI\n\n\n![manage_fastapi](assets/manage_fastapi.gif)\n\n<p align="center">\n    <a href="https://github.com/ycd/manage-fastapi" target="_blank">\n        <img src="https://img.shields.io/github/last-commit/ycd/manage-fastapi?style=for-the-badge" alt="Latest Commit">\n    </a>\n        <img src="https://img.shields.io/github/workflow/status/ycd/manage-fastapi/Test?style=for-the-badge">\n        <img src="https://img.shields.io/codecov/c/github/ycd/manage-fastapi?style=for-the-badge">\n    <br />\n    <a href="https://pypi.org/project/manage-fastapi" target="_blank">\n        <img src="https://img.shields.io/pypi/v/manage-fastapi?style=for-the-badge" alt="Package version">\n    </a>\n    <img src="https://img.shields.io/pypi/pyversions/manage-fastapi?style=for-the-badge">\n    <img src="https://img.shields.io/github/license/ycd/manage-fastapi?style=for-the-badge">\n</p>\n</div>\n\n\n---\n\n**Source Code**: View it on [Github](https://github.com/ycd/manage-fastapi/)\n\n---\n\n\n##  Features 🚀\n\n* #### Creates customizable **project boilerplate.**\n* #### Creates customizable **app boilerplate.**\n* #### Handles the project structuring for you.\n* #### Optional Dockerfile generation.\n* #### Optional docker-compose generation for your project needs.\n* #### Optional pre-commit hook generation.\n\n\n## Installation 📌\n\n* Prerequisites\n    * Python 3.6 +\n\nManage FastAPI can be installed by running \n\n```python\npip install manage-fastapi \n```\n\n\n## Getting started 🎈\n\nEasiest way to start is using the defaults:\n\n```bash\nfastapi startproject [name]\n```\n\nBut there is an **interactive** mode!\n\n```bash\nfastapi startproject [name] --interactive\n```\n\n\n\n## Command line options 🧰\n\nManage FastAPI provides three different commands. \n\nYou can list them with\n\n```bash\nfastapi --help\n```\n\n<img src="docs/docs_assets/fastapi-help.png" width=600>\n\nThe idea is to have a highly customizable CLI, but at the same time a simple interface for new users. You can see the available options for `startproject` running `fastapi startproject --help`:\n\n<img src="docs/docs_assets/startproject-help.png" width=600>\n\nThe other commands are already available but the current implementation is too shallow. More details about `startapp` and `run` commands will be provided once they have more functionalities, at the moment you can run `startapp` by just:\n\n```bash\nfastapi startapp {name}\n```\n\nOn the other hand, the `run` command expects you to have a `startproject` structure:\n\n```bash\nfastapi run\n```\n\n## License\n\nThis project is licensed under the terms of the MIT license.\n',
    'author': 'ycd',
    'author_email': 'yagizcanilbey1903@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ycd/manage-fastapi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
