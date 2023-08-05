# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_git_version_changer']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'poetry-git-version-changer',
    'version': '1.0.0a0',
    'description': 'An extension to support dynamic package versioning with poetry.',
    'long_description': '```toml\n[tool.poetry.git-version-changer]\nenabled = true\nversion-file = "foo/__init__.py"\n```\n',
    'author': 'Bijij',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bijij/unnamed-poetry-extension',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
