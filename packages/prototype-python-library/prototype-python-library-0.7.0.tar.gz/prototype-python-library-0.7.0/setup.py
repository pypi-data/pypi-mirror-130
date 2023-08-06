# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['prototype_python_library']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'prototype-python-library',
    'version': '0.7.0',
    'description': 'A prototype python library.',
    'long_description': '# Python Package\n\n[![Built with Cookiecutter Python Package](https://img.shields.io/badge/built%20with-Cookiecutter%20Python%20Package-ff69b4.svg?logo=cookiecutter)](https://github.com/91nunocosta/python-package-cookiecutter)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Codacy Badge](https://app.codacy.com/project/badge/Grade/cb92f3f137454fae8697c7a6e7334f74)](https://www.codacy.com/gh/91nunocosta/prototype-python-library/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=91nunocosta/prototype-python-library&amp;utm_campaign=Badge_Grade)\n[![codecov](https://codecov.io/gh/91nunocosta/python-package/branch/master/graph/badge.svg?token=7T24BIO7QU)](https://codecov.io/gh/91nunocosta/python-package)\n![PyPI - License](https://img.shields.io/pypi/l/prototype-python-library)\n![PyPI](https://img.shields.io/pypi/v/prototype-python-library)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/prototype-python-library)\n![PyPI - Wheel](https://img.shields.io/pypi/wheel/prototype-python-library)\n[![docs](https://readthedocs.org/projects/prototype-python-package/badge/?version=latest)](https://prototype-python-package.readthedocs.io/en/latest/)\n\nAn empty python package.\n\n## Usage\n\nRead the [documentation](https://prototype-python-package.readthedocs.io/en/latest/).\n\n## Contributing\n\nIf you want to contribute, please read the [contributing guidelines](./CONTRIBUTING.md)\nand [code of conduct](./CODE_OF_CONDUCT.md).\n',
    'author': 'Nuno Costa',
    'author_email': '91nunocosta@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/91nunocosta/prototype-python-library/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
