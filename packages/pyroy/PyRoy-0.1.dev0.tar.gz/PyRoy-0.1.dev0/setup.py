# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyroy']

package_data = \
{'': ['*']}

install_requires = \
['typing_extensions>=4.0.1']

setup_kwargs = {
    'name': 'pyroy',
    'version': '0.1.dev0',
    'description': '',
    'long_description': '=====\nPyRoy\n=====\n|ReadTheDocs| |PyPI release| |License| |PyPI downloads| |Python versions| |GitHub CI| |Codecov|\n\n.. |ReadTheDocs| image:: https://readthedocs.org/projects/pyroy/badge/?version=latest\n  :target: https://pyroy.readthedocs.io/en/latest/?badge=latest\n  :alt: Build status on Read The Docs\n\n.. |PyPI release| image:: https://badge.fury.io/py/pyroy.svg\n  :target: https://pypi.org/project/pyroy/\n  :alt: Stable release on PyPI\n\n.. |Python versions| image:: https://img.shields.io/badge/Python-3.10-blue\n  :target: https://pypi.org/project/pyroy/\n  :alt: Supported versions of Python\n\n.. |PyPI downloads| image:: https://static.pepy.tech/personalized-badge/pyroy?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Downloads\n  :target: https://pepy.tech/project/pyroy\n  :alt: Count of downloads from PyPI\n\n.. |License| image:: https://img.shields.io/badge/License-MIT-blue\n  :target: https://github.com/cslibs/pyroy/blob/master/LICENSE\n  :alt: MIT License\n\n.. |GitHub CI| image:: https://github.com/cslibs/pyroy/actions/workflows/ci.yml/badge.svg?branch=master\n  :target: https://github.com/cslibs/pyroy/actions/workflows/ci.yml\n  :alt: Status of continuous integration on GitHub Actions\n\n.. |Codecov| image:: https://codecov.io/gh/cslibs/pyroy/branch/master/graph/badge.svg\n  :target: https://codecov.io/gh/cslibs/pyroy\n  :alt: Status of test coverage on codecov.io\n\nDocumentation\n-------------\nhttps://pyroy.readthedocs.io\n\nInstallation\n------------\nInstall PyRoy with pip: ::\n\n  pip install pyroy\n',
    'author': 'Ruslan Ilyasovich Gilfanov',
    'author_email': 'ri.gilfanov@yandex.ru',
    'maintainer': 'Ruslan Ilyasovich Gilfanov',
    'maintainer_email': 'ri.gilfanov@yandex.ru',
    'url': 'https://pypi.org/project/pyroy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
