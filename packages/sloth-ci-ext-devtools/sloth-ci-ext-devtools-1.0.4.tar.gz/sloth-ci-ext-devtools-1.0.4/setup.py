# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['templates']

package_data = \
{'': ['*']}

modules = \
['sloth_ci_ext_devtools']
install_requires = \
['sloth-ci>=2.2,<3.0']

setup_kwargs = {
    'name': 'sloth-ci-ext-devtools',
    'version': '1.0.4',
    'description': 'Utilities to help you develop extensions and validators for Sloth CI',
    'long_description': '# Utilities to help developers create validators and extensions for Sloth CI\n\n\n## Installation\n    \n    $ pip install sloth-ci-ext-devtools\n\n\n## Usage\n\nEnable the extension in the server config:\n\n    extensions:\n        dev:\n            # Use the module sloth_ci.ext.devtools.\n            module: devtools\n\nCall `sci dev` with `-e` or `-v` to create an extensions or a validator template:\n\n    $ sci dev -e spam\n    Extension "spam" created.\n    $ sci dev -v eggs\n    Validator "eggs" created.\n',
    'author': 'Constantine Molchanov',
    'author_email': 'moigagoo@live.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
