# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dazvol']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dazvol',
    'version': '0.1.0',
    'description': 'Authorization library for Python.',
    'long_description': '# Dazvol\n\nAuthorization library for Python.\n\n![PyPI](https://img.shields.io/pypi/v/dazvol)\n![GitHub Workflow Status](https://img.shields.io/github/workflow/status/alex-oleshkevich/dazvol/Lint)\n![GitHub](https://img.shields.io/github/license/alex-oleshkevich/dazvol)\n![Libraries.io dependency status for latest release](https://img.shields.io/librariesio/release/pypi/dazvol)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/dazvol)\n![GitHub Release Date](https://img.shields.io/github/release-date/alex-oleshkevich/dazvol)\n![Lines of code](https://img.shields.io/tokei/lines/github/alex-oleshkevich/dazvol)\n\n## Installation\n\nInstall `dazvol` using PIP or poetry:\n\n```bash\npip install dazvol\n# or\npoetry add dazvol\n```\n\n## Features\n\n-   TODO\n\n## Quick start\n\nSee example application in `examples/` directory of this repository.\n',
    'author': 'Alex Oleshkevich',
    'author_email': 'alex.oleshkevich@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/alex-oleshkevich/dazvol',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
