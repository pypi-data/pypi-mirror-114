# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mark1_translate']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'mark1-translate',
    'version': '0.1.2',
    'description': '',
    'long_description': "# Mark1 Translator\n\nThis is a small tool to translate from Google Translate, base on mtranslate by [mouuff](https://github.com/mouuff)\n\nIt was reduce to the minimum expression and converted to use requests\n\n# Install\nIt is highly recommended to use it inside a virtual enviroment for your project, but can be install globally\n\nNote: this instructions are made for ubuntu\n\n```bash\n$ pip3 install mark1_translate\n```\n\n```bash\n$ virtualenv .venv\n$ source .venv/bin/activate\n$ pip install mark1_translate\n$ python3\n```\n\n# Example\n\n## On interactive console type\n\n```py\n>>> from mark1_translate imprt translate\n>>> translate('hola mundo', 'en', 'auto')\n'Hello World'\n```\n\n## On a project\n\n```py\nfrom mark1_translate imprt translate\n\nt = translate('hola mundo', 'en', 'auto')\n\nprint(t)\n```\n\n\n",
    'author': 'cgmark101',
    'author_email': 'cgmark101@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
