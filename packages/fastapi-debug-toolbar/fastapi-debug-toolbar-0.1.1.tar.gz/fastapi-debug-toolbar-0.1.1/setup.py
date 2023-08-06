# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['debug_toolbar', 'debug_toolbar.panels']

package_data = \
{'': ['*'],
 'debug_toolbar': ['statics/css/*',
                   'statics/img/*',
                   'statics/js/*',
                   'templates/*',
                   'templates/includes/*',
                   'templates/panels/*']}

install_requires = \
['Jinja2>=2.9',
 'aiofiles>=0.2.1',
 'fastapi>=0.62.0',
 'pyinstrument>=3.0.0',
 'sqlparse>=0.2.0']

setup_kwargs = {
    'name': 'fastapi-debug-toolbar',
    'version': '0.1.1',
    'description': 'A debug toolbar for FastAPI.',
    'long_description': '# ![FastAPI](https://raw.githubusercontent.com/mongkok/fastapi-debug-toolbar/main/debug_toolbar/statics/img/icon-green.svg) Debug Toolbar\n\n<p align="center">\n    <a href="https://fastapi-debug-toolbar.domake.io">\n        <img src="https://user-images.githubusercontent.com/5514990/127749737-1a2b5ce7-a191-4f8b-96e4-fe94e0a08f6f.gif" alt="FastAPI Debug Toolbar">\n    </a>\n</p>\n<p align="center">\n    <em>🐞A debug toolbar for FastAPI based on the original django-debug-toolbar.🐞</em>\n    <br><em><b>Swagger UI</b> & <b>GraphQL</b> are supported.</em>\n</p>\n<p align="center">\n<a href="https://github.com/mongkok/fastapi-debug-toolbar/actions">\n    <img src="https://github.com/mongkok/fastapi-debug-toolbar/actions/workflows/test-suite.yml/badge.svg" alt="Test">\n</a>\n<a href="https://codecov.io/gh/mongkok/fastapi-debug-toolbar">\n    <img src="https://img.shields.io/codecov/c/github/mongkok/fastapi-debug-toolbar?color=%2334D058" alt="Coverage">\n</a>\n<a href="https://www.codacy.com/gh/mongkok/fastapi-debug-toolbar/dashboard">\n    <img src="https://app.codacy.com/project/badge/Grade/e9d8ba3973264424a3296016063b4ab5" alt="Codacy">\n</a>\n<a href="https://pypi.org/project/fastapi-debug-toolbar">\n    <img src="https://img.shields.io/pypi/v/fastapi-debug-toolbar" alt="Package version">\n</a>\n\n---\n\n**Documentation**: [https://fastapi-debug-toolbar.domake.io](https://fastapi-debug-toolbar.domake.io)\n\n---\n\n## Installation\n\n```sh\npip install fastapi-debug-toolbar\n```\n\n## Quickstart\n\nAdd `DebugToolbarMiddleware` middleware to your FastAPI application:\n\n```py\nfrom debug_toolbar.middleware import DebugToolbarMiddleware\nfrom fastapi import FastAPI\n\napp = FastAPI(debug=True)\napp.add_middleware(DebugToolbarMiddleware)\n```\n\n## SQLAlchemy\n\nPlease make sure to use the *"Dependency Injection"* system as described in the [FastAPI docs](https://fastapi.tiangolo.com/tutorial/sql-databases/#create-a-dependency) and add the SQLAlchemy panel to the argument list of the Debug Toolbar middleware:\n\n```py\napp.add_middleware(\n    DebugToolbarMiddleware,\n    panels=["debug_toolbar.panels.sqlalchemy.SQLAlchemyPanel"],\n)\n```\n',
    'author': 'Dani',
    'author_email': 'dani@domake.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mongkok/fastapi-debug-toolbar',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
