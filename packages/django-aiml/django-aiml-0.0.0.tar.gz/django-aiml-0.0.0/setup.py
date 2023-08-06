# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['django_aiml']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0']

entry_points = \
{'console_scripts': ['django-aiml = django_aiml.__main__:main']}

setup_kwargs = {
    'name': 'django-aiml',
    'version': '0.0.0',
    'description': 'Django AIML',
    'long_description': "Django AIML\n===========\n\n|PyPI| |Status| |Python Version| |License|\n\n|Read the Docs| |Tests| |Codecov|\n\n|pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/django-aiml.svg\n   :target: https://pypi.org/project/django-aiml/\n   :alt: PyPI\n.. |Status| image:: https://img.shields.io/pypi/status/django-aiml.svg\n   :target: https://pypi.org/project/django-aiml/\n   :alt: Status\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/django-aiml\n   :target: https://pypi.org/project/django-aiml\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/django-aiml\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/django-aiml/latest.svg?label=Read%20the%20Docs\n   :target: https://django-aiml.readthedocs.io/\n   :alt: Read the documentation at https://django-aiml.readthedocs.io/\n.. |Tests| image:: https://github.com/jeffmaxey/django-aiml/workflows/Tests/badge.svg\n   :target: https://github.com/jeffmaxey/django-aiml/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/jeffmaxey/django-aiml/branch/main/graph/badge.svg\n   :target: https://codecov.io/gh/jeffmaxey/django-aiml\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\n\nFeatures\n--------\n\n* TODO\n\n\nRequirements\n------------\n\n* TODO\n\n\nInstallation\n------------\n\nYou can install *Django AIML* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install django-aiml\n\n\nUsage\n-----\n\nPlease see the `Command-line Reference <Usage_>`_ for details.\n\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the `MIT license`_,\n*Django AIML* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\nCredits\n-------\n\nThis project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.\n\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _MIT license: https://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _file an issue: https://github.com/jeffmaxey/django-aiml/issues\n.. _pip: https://pip.pypa.io/\n.. github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n.. _Usage: https://django-aiml.readthedocs.io/en/latest/usage.html\n",
    'author': 'Jeff A. Maxey',
    'author_email': 'jeffmaxey@comcast.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jeffmaxey/django-aiml',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
