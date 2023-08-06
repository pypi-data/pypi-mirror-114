# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stupidb']

package_data = \
{'': ['*']}

install_requires = \
['cytoolz>=0.11.0,<0.12.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=4.6.1,<5.0.0'],
 'animation': ['pydot>=1.4.2,<2.0.0']}

setup_kwargs = {
    'name': 'stupidb',
    'version': '4.4.0',
    'description': 'The stupidest of all the databases.',
    'long_description': "=======\nStupiDB\n=======\n\n.. image:: https://img.shields.io/pypi/v/stupidb.svg\n        :target: https://pypi.python.org/pypi/stupidb\n\n.. image:: https://github.com/cpcloud/stupidb/actions/workflows/ci.yml/badge.svg?branch=master\n        :target: https://github.com/cpcloud/stupidb/actions/workflows/ci.yml\n\n.. image:: https://readthedocs.org/projects/stupidb/badge/?version=latest\n        :target: https://stupidb.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n\nAre you tired of software that's too smart? Try StupiDB, the stupidest database\nyou'll ever come across.\n\nStupiDB was built to understand how a relational database might be implemented.\n\nRDBMSs like PostgreSQL are extremely complex. It was hard for to me to imagine\nwhat implementing the core of a relational database like PostgreSQL would look\nlike just by tinkering with and reading the source code, so I decided to write\nmy own.\n\n* Free software: Apache Software License 2.0\n* Documentation: https://stupidb.readthedocs.io.\n\nFeatures\n--------\n* Stupid joins\n* Idiotic window functions\n* Woefully naive set operations\n* Sophomoric group bys\n* Dumb custom aggregates\n* Scales down, to keep expectations low\n* Wildly cloud unready\n* Worst-in-class performance\n\nNon-Features\n------------\n* Stupid simple in-memory format: ``Iterable[Mapping[str, Any]]``\n* Stupidly clean codebase\n\nCredits\n-------\nThis package was created with Cookiecutter_ and the\n`audreyr/cookiecutter-pypackage`_ project template.\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage\n",
    'author': 'Phillip Cloud',
    'author_email': 'cpcloud@gmail.com',
    'maintainer': 'Phillip Cloud',
    'maintainer_email': 'cpcloud@gmail.com',
    'url': 'https://github.com/cpcloud/stupidb',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
