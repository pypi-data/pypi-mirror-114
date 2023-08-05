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
    'version': '0.1.7',
    'description': 'django-fsm data immutability support',
    'long_description': "# django fsm data immutability support\n![CI](https://github.com/ming-tung/django-fsm-freeze/actions/workflows/continues-integration.yml/badge.svg?branch=main)\n[![PyPI version](https://badge.fury.io/py/django-fsm-freeze.svg)](https://badge.fury.io/py/django-fsm-freeze)\n[![Downloads](https://static.pepy.tech/personalized-badge/django-fsm-freeze?period=total&units=international_system&left_color=grey&right_color=yellowgreen&left_text=Downloads)](https://pepy.tech/project/django-fsm-freeze)\n\ndjango-fsm-freeze provides a django model mixin for data immutability based on\n[django-fsm](https://github.com/viewflow/django-fsm).\n\n\n## Installation\n\n```commandline\npip install django-fsm-freeze\n```\n\n## Usage\n\n- Add `FreezableFSMModelMixin` to your [django-fsm](https://github.com/viewflow/django-fsm) model\n- Specify the `FROZEN_IN_STATES` in which the object should be frozen, meaning the\n  value of its fields/attributes cannot be changed.\n- (optional) Customize the `NON_FROZEN_FIELDS` for mutability\n\nWhen an object is in a frozen state, by default all of its fields are immutable,\nexcept for the `state` field which needs to be mutable for\n[django-fsm](https://github.com/viewflow/django-fsm) to work.\n\nIn case we still want to mutate certain fields when the object is frozen, we can override\nthe `NON_FROZEN_FIELDS` to allow it.\nWhen overriding the `NON_FROZEN_FIELDS`, be careful to include `state` for the reason\nmentioned above.\n\n\n```python\nfrom django.db import models\nfrom django_fsm import FSMField\n\nfrom django_fsm_freeze.models import FreezableFSMModelMixin\n\nclass MyDjangoFSMModel(FreezableFSMModelMixin, models.Model):\n\n    # In this example, when object is in the 'active' state, it is immutable.\n    FROZEN_IN_STATES = ('active', )\n\n    NON_FROZEN_FIELDS = FreezableFSMModelMixin.NON_FROZEN_FIELDS + (\n        'a_mutable_field',\n    )\n    # This field is mutable even when the object is in the frozen state.\n    a_mutable_field = models.BooleanField()\n\n    # django-fsm specifics: state, transitions, etc.\n    state = FSMField(default='new')\n    # ...\n\n```\n\nSee example usage also in https://github.com/ming-tung/django-fsm-freeze/blob/main/mytest/models.py\n",
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
