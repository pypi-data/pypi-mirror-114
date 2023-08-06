# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['workspace']

package_data = \
{'': ['*'],
 'workspace': ['.git/*',
               '.git/hooks/*',
               '.git/info/*',
               '.git/logs/*',
               '.git/objects/09/*',
               '.git/objects/4b/*',
               '.git/objects/4c/*',
               '.git/objects/53/*',
               '.git/objects/58/*',
               '.git/objects/77/*',
               '.git/objects/a2/*',
               '.git/objects/a3/*',
               '.git/objects/b2/*',
               '.git/objects/d5/*',
               '.git/objects/d9/*',
               '.git/refs/tags/*',
               '.github/workflows/*']}

install_requires = \
['Shapely>=1.7.1,<2.0.0',
 'mapbox-vector-tile>=1.2.1,<2.0.0',
 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'deutschland',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Lilith Wittmann',
    'author_email': 'mail@lilithwittmann.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
