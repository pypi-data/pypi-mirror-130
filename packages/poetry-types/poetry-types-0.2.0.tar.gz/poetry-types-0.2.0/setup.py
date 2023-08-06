# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_types', 'poetry_types.commands']

package_data = \
{'': ['*']}

install_requires = \
['poetry>=1.2.0a2,<2.0.0']

entry_points = \
{'poetry.application.plugin': ['poetry-types = '
                               'poetry_types.poetry_types:PoetryTypes']}

setup_kwargs = {
    'name': 'poetry-types',
    'version': '0.2.0',
    'description': 'A poetry plugin that automatically adds type subs as dependencies like the mypy --install-types command.',
    'long_description': '# poetry-types\n\nThis is a plugin to poetry for the upcoming poetry 1.2 plugin feature.\nIt automatically installs/removes typing stubs when adding, removing or updating packages via commands.\nAdditionally, there are commands you can use to trigger this plugins behaviour:\n\n- `poetry types add <package names>`\n- `poetry types remove <package names>`\n- `poetry types update`\n\n## Installation\n\nRun `poetry plugin add poetry-plugin`\n\nNote: With poetry version 1.2.0a2 poetry removes all dependencies when using `poetry remove` and so does\n`poetry types remove`. Using poetry from the git repo is recommended when testing this plugin.\n\n## TODO:\n\n- Add tests\n- Make command-line output more beautiful maybe?\n',
    'author': 'kreyoo',
    'author_email': 'zunder325@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kreyoo/poetry-types',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
