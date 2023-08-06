# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ogadf_schema']

package_data = \
{'': ['*']}

install_requires = \
['fits-schema>=0.5.4,<0.6.0']

setup_kwargs = {
    'name': 'ogadf-schema',
    'version': '0.2.4.post1',
    'description': 'Schema definitions for the Data Formats For Gamma-Ray Astronomy',
    'long_description': '# ogadf-schema\n\nDefinition of the open gamma ray astronomy data formats using fits-schema\n\n\n## WARNING\n\nThis is not the canonical source of this specification.\nIf you find disagreements between this package and the official specifications\nat https://gamma-astro-data-formats.readthedocs.io/en/latest/index.html, please\nopen an issue here.\n',
    'author': 'Maximilian Nöthe',
    'author_email': 'maximilian.noethe@tu-dortmund.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
