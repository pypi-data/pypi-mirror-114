# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_fsm_freeze']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.1.12,<3.2.0',
 'django-dirtyfields>=1.7.0,<2.0.0',
 'django-fsm>=2.7.1,<3.0.0']

setup_kwargs = {
    'name': 'django-fsm-freeze',
    'version': '0.1.6',
    'description': 'django-fsm data immutability support',
    'long_description': None,
    'author': 'ming-tung',
    'author_email': 'mingtung.hong@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ming-tung/django-fsm-freeze',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
