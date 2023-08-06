# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dj_datatables_view']

package_data = \
{'': ['*']}

install_requires = \
['Django>=4.0,<5.0']

setup_kwargs = {
    'name': 'dj-datatables-view',
    'version': '0.1.0',
    'description': 'Django datatables view fork from django-datatables-view',
    'long_description': None,
    'author': 'Longbowou',
    'author_email': 'blandedaniel@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
