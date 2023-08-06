# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pytest_aioresponses']
install_requires = \
['aioresponses>=0.7.1,<0.8.0', 'pytest-asyncio>=0.14.0', 'pytest>=3.5.0']

entry_points = \
{'pytest11': ['aioresponses = pytest_aioresponses']}

setup_kwargs = {
    'name': 'pytest-aioresponses',
    'version': '0.2.0',
    'description': 'py.test integration for aioresponses',
    'long_description': '===================\npytest-aioresponses\n===================\n\n.. image:: https://img.shields.io/pypi/v/pytest-aioresponses.svg\n    :target: https://pypi.org/project/pytest-aioresponses\n    :alt: PyPI version\n\n.. image:: https://img.shields.io/pypi/pyversions/pytest-aioresponses.svg\n    :target: https://pypi.org/project/pytest-aioresponses\n    :alt: Python versions\n\nAn integration of `aioresponses`_ for `py.test`_ similar to `pytest-responses`_\n\n----\n\nInstallation\n------------\n\nYou can install "pytest-aioresponses" via `pip`_ from `PyPI`_::\n\n    $ pip install pytest-aioresponses\n\n\nUsage\n-----\n\n.. sourcecode:: python\n\n\n    import aiohttp\n    import pytest\n\n    @pytest.mark.asyncio\n    async def test_something(aioresponses):\n        aioresponses.get("https://hello.aio")\n\n        async with aiohttp.ClientSession() as session:\n            async with session.get("https://hello.aio") as response:\n                assert response.status == 200\n\nContributing\n------------\nContributions are very welcome.\n\nLicense\n-------\n\nDistributed under the terms of the `MIT`_ license, "pytest-aioresponses" is free and open source software\n\n\nIssues\n------\n\nIf you encounter any problems, please `file an issue`_ along with a detailed description.\n\n.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter\n.. _`@hackebrot`: https://github.com/hackebrot\n.. _`MIT`: http://opensource.org/licenses/MIT\n.. _`BSD-3`: http://opensource.org/licenses/BSD-3-Clause\n.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt\n.. _`Apache Software License 2.0`: http://www.apache.org/licenses/LICENSE-2.0\n.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin\n.. _`file an issue`: https://github.com/pheanex/pytest-aioresponses/issues\n.. _`pytest`: https://github.com/pytest-dev/pytest\n.. _`tox`: https://tox.readthedocs.io/en/latest/\n.. _`pip`: https://pypi.org/project/pip/\n.. _`PyPI`: https://pypi.org/project/pytest-aioresponses/\n.. _`aioresponses`: https://pypi.org/project/aioresponses/\n.. _`pytest-responses`: https://pypi.org/project/pytest-responses/\n.. _`py.test`: https://pypi.org/project/pytest/',
    'author': 'Konstantin Manna',
    'author_email': 'Konstantin@Manna.uno',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pheanex/pytest-aioresponses',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
