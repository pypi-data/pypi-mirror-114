# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['decoratemethod']
setup_kwargs = {
    'name': 'decoratemethod',
    'version': '0.1.1',
    'description': 'Let function decorator decorate the bound method of per instance.',
    'long_description': '# decoratemethod\n\nLet function decorator decorate the bound method for each instance.\n\n## Usage\n\n### lru_cache\n\nTo let each instance has their own lru cache:\n\n``` py\nfrom functools import lru_cache\nfrom decoratemethod import decorate\n\nclass Foo:\n    @decorate(lru_cache)\n    def decorated_method(self, x):\n        ...\n```\n',
    'author': 'Cologler',
    'author_email': 'skyoflw@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Cologler/decoratemethod-python',
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
