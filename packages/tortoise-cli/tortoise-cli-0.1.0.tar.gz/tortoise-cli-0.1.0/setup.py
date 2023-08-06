# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tortoise_cli']

package_data = \
{'': ['*']}

install_requires = \
['click', 'ptpython', 'tortoise-orm']

entry_points = \
{'console_scripts': ['tortoise-cli = tortoise_cli.cli:main']}

setup_kwargs = {
    'name': 'tortoise-cli',
    'version': '0.1.0',
    'description': 'A cli tool for tortoise-orm, build on top of click and ptpython.',
    'long_description': '# tortoise-cli\n\n[![image](https://img.shields.io/pypi/v/tortoise-cli.svg?style=flat)](https://pypi.python.org/pypi/tortoise-cli)\n[![image](https://img.shields.io/github/license/tortoise/tortoise-cli)](https://github.com/tortoise/tortoise-cli)\n[![image](https://github.com/tortoise/tortoise-cli/workflows/pypi/badge.svg)](https://github.com/tortoise/tortoise-cli/actions?query=workflow:pypi)\n\nA cli tool for tortoise-orm, build on top of click and ptpython.\n\n## Installation\n\nYou can just install from pypi.\n\n```shell\npip install tortoise-cli\n```\n\n## Quick Start\n\n```shell\n> tortoise-cli -h                                                                                                                                                                 23:59:38\nUsage: tortoise-cli [OPTIONS] COMMAND [ARGS]...\n\nOptions:\n  -V, --version      Show the version and exit.\n  -c, --config TEXT  TortoiseORM config dictionary path, like\n                     settings.TORTOISE_ORM  [required]\n  -h, --help         Show this message and exit.\n\nCommands:\n  shell  Start an interactive shell.\n```\n\n## Usage\n\nFirst, you need make a TortoiseORM config object, assuming that in `settings.py`.\n\n```python\nTORTOISE_ORM = {\n    "connections": {\n        "default": \'sqlite://:memory:\',\n    },\n    "apps": {\n        "models": {"models": ["examples.models"], "default_connection": "default"},\n    },\n}\n```\n\n## Interactive shell\n\nThen you can start an interactive shell for TortoiseORM.\n\n```shell\ntortoise-cli -c settings.TORTOISE_ORM shell\n```\n\nOr you can set config by set environment variable.\n\n```shell\nexport TORTOISE_ORM=settings.TORTOISE_ORM\n```\n\nThen just run:\n\n```shell\ntortoise-cli shell\n```\n\n## License\n\nThis project is licensed under the\n[Apache-2.0](https://github.com/tortoise/tortoise-cli/blob/main/LICENSE) License.\n',
    'author': 'long2ice',
    'author_email': 'long2ice@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tortoise/tortoise-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
