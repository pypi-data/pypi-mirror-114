# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['django_shared_property']

package_data = \
{'': ['*']}

install_requires = \
['astor']

setup_kwargs = {
    'name': 'django-shared-property',
    'version': '0.2.5',
    'description': 'Properties that are both ORM expressions and python code.',
    'long_description': '======================\nDjango Shared Property\n======================\n\n\n.. image:: https://img.shields.io/pypi/v/django_shared_property.svg\n        :target: https://pypi.python.org/pypi/django_shared_property\n\n.. image:: https://img.shields.io/travis/schinckel/django-shared-property.svg\n        :target: https://travis-ci.org/schinckel/django-shared-property\n\n.. image:: https://ci.appveyor.com/api/projects/status/schinckel/branch/main?svg=true\n    :target: https://ci.appveyor.com/project/schinckel/django-shared-property/branch/main\n    :alt: Build status on Appveyor\n\n.. image:: https://readthedocs.org/projects/django-shared-property/badge/?version=latest\n        :target: https://django-shared-property.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n\n\n\n\nProperties that are both ORM expressions and python code.\n\n\n* Free software: MIT license\n\n* Documentation: https://django-shared-property.readthedocs.io.\n\n\n\nInstallation:\n-------------\n\n.. code-block:: console\n\n    $ pip install django_shared_property\n\nFeatures\n--------\n\n* TODO\n\nCredits\n-------\n\nThis package was created with Cookiecutter_ and the `wboxx1/cookiecutter-pypackage-poetry`_ project template.\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`wboxx1/cookiecutter-pypackage-poetry`: https://github.com/wboxx1/cookiecutter-pypackage-poetry\n',
    'author': 'Matthew Schinckel',
    'author_email': 'matt@schinckel.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://django-shared-property.readthedocs.io',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>3.8',
}


setup(**setup_kwargs)
