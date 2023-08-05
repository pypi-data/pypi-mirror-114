# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydelegate']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pydelegate',
    'version': '0.2.0',
    'description': 'a python version delegate like C#',
    'long_description': "# pydelegate\n\n![GitHub](https://img.shields.io/github/license/Cologler/pydelegate-python.svg)\n[![Build Status](https://travis-ci.com/Cologler/pydelegate-python.svg?branch=master)](https://travis-ci.com/Cologler/pydelegate-python)\n[![PyPI](https://img.shields.io/pypi/v/pydelegate.svg)](https://pypi.org/project/pydelegate/)\n\na python version delegate like C#.\n\n## Usage\n\n``` py\nfrom pydelegate import Delegate\n\ndef func():\n    return 1\n\nd = Delegate()\nd += func\nassert d() == 1\n```\n\nor you can set init `Delegate` lazy:\n\n``` py\nfrom pydelegate import event_handler\n\ndef func():\n    return 1\n\nd = None\nd += event_handler(func) # event_handler() return a `Delegate`\nassert d() == 1\n```\n\nor if you want inject `self` var in your instance method, use `event` data descriptor:\n\n``` py\nfrom pydelegate import event\n\nclass A:\n    @event\n    def d(self):\n        pass\n    # or\n    e = event('e')\n\ndef func(self):\n    return 1\n\na = A()\na.d += func\nassert a.d() == 1\n```\n\nread unittests for more usages.\n",
    'author': 'Cologler',
    'author_email': 'skyoflw@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Cologler/pydelegate-python',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
