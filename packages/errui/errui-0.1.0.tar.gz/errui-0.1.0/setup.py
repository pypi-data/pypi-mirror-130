# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['errui']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'errui',
    'version': '0.1.0',
    'description': 'Error handling for end users',
    'long_description': '# ErrUI\n\nOpen a window when an exception is raised and prompt the end user to decide what to do.\n\n\n## Installation\n\n```sh\npython -m pip install errui\n```\n\n## Example\n\n### `AbortWindow` (Optional suppression)\n\nThis is like `contextlib.suppress` except you get to choose whether to suppress it or to let the exception through and still be raised.\n\n```py\nfrom errui import AbortWindow\n\nwith AbortWindow(KeyError):\n    {}[0]\n```',
    'author': 'Maximillian Strand',
    'author_email': 'maximillian.strand@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/deepadmax/errui',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
