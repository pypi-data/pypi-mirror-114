# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['omniblack',
 'omniblack.model',
 'omniblack.model.structs',
 'omniblack.model.types']

package_data = \
{'': ['*'], 'omniblack.model': ['model/*']}

install_requires = \
['anyio>=3.0.0,<4.0.0',
 'atpublic>=2.3,<3.0',
 'humanize>=3.4.1,<4.0.0',
 'more_itertools>=8.7.0,<9.0.0',
 'rx>=3.1.1,<4.0.0',
 'sniffio>=1.2.0,<2.0.0']

extras_require = \
{'toml': ['toml>=0.10.2,<0.11.0'], 'yaml': ['ruamel.yaml>=0.16.12,<0.17.0']}

setup_kwargs = {
    'name': 'omniblack.model',
    'version': '0.1.16',
    'description': 'A library enabling model driven development.',
    'long_description': None,
    'author': 'Terry Patterson',
    'author_email': 'Terryp@wegrok.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
