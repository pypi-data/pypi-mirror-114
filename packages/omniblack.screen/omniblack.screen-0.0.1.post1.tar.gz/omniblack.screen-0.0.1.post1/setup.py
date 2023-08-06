# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['omniblack', 'omniblack.screen']

package_data = \
{'': ['*']}

install_requires = \
['urwid>=2.1.2,<3.0.0']

setup_kwargs = {
    'name': 'omniblack.screen',
    'version': '0.0.1.post1',
    'description': 'A screen displaying running build processes.',
    'long_description': None,
    'author': 'Terry Patterson',
    'author_email': 'terryp@wegrok.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
