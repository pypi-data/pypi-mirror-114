# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['imia']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'imia',
    'version': '0.1.0',
    'description': 'Full stack authentication library for ASGI.',
    'long_description': '# Imia\n\nFull stack authentication library for ASGI.\n\n![PyPI](https://img.shields.io/pypi/v/imia)\n![GitHub Workflow Status](https://img.shields.io/github/workflow/status/alex-oleshkevich/imia/Lint)\n![GitHub](https://img.shields.io/github/license/alex-oleshkevich/imia)\n![Libraries.io dependency status for latest release](https://img.shields.io/librariesio/release/pypi/imia)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/imia)\n![GitHub Release Date](https://img.shields.io/github/release-date/alex-oleshkevich/imia)\n![Lines of code](https://img.shields.io/tokei/lines/github/alex-oleshkevich/imia)\n\n## Installation\n\nInstall `imia` using PIP or poetry:\n\n```bash\npip install imia\n# or\npoetry add imia\n```\n\n## Features\n\n-   TODO\n\n## Quick start\n\nSee example application in `examples/` directory of this repository.\n',
    'author': 'Alex Oleshkevich',
    'author_email': 'alex.oleshkevich@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/alex-oleshkevich/imia',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
