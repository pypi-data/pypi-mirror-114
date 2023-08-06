# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydbrepo',
 'pydbrepo.descriptors',
 'pydbrepo.drivers',
 'pydbrepo.entity',
 'pydbrepo.errors',
 'pydbrepo.helpers',
 'pydbrepo.helpers.common',
 'pydbrepo.helpers.mongo',
 'pydbrepo.helpers.sql',
 'pydbrepo.repository']

package_data = \
{'': ['*']}

install_requires = \
['PyPika>=0.48.7,<0.49.0', 'python-dateutil>=2.8.2,<3.0.0']

setup_kwargs = {
    'name': 'pydbrepo',
    'version': '0.1.6',
    'description': 'Simple implementation of repository pattern for database connections.',
    'long_description': '# PyDBRepo\n\nIs a simple implementation of the Repository pattern to access data in python, providing extensibility flexibility\nand builtin tools to manage databases with this pattern.\n\n## Requirements\n\n- Python >= 3.7\n  \n### Postgres\n\n- psychopg2-binary\n  \n### MongoDB\n\n- pymongo\n- dnspython\n',
    'author': 'Eduardo Aguilar',
    'author_email': 'dante.aguilar41@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/danteay/pydbrepo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
