# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['trading_ig']

package_data = \
{'': ['*']}

install_requires = \
['pycryptodome>=3.9,<4.0',
 'requests-cache>=0.5,<0.6',
 'requests>=2.24,<3.0',
 'six>=1.15,<2.0']

extras_require = \
{'docs': ['Sphinx>=4.0.3,<5.0.0'],
 'munch': ['munch>=2.5,<3.0'],
 'pandas': ['pandas>=1,<2'],
 'sphinx': ['Sphinx>=4.0.3,<5.0.0'],
 'tenacity': ['tenacity>=7.0,<8.0']}

setup_kwargs = {
    'name': 'trading-ig',
    'version': '0.0.12',
    'description': 'A lightweight wrapper for the IG Markets API written in Python',
    'long_description': '.. image:: https://img.shields.io/pypi/v/trading_ig.svg\n    :target: https://pypi.python.org/pypi/trading_ig/\n    :alt: Latest Version\n\n.. image:: https://img.shields.io/pypi/pyversions/trading_ig.svg\n    :target: https://pypi.python.org/pypi/trading_ig/\n    :alt: Supported Python versions\n\n.. image:: https://img.shields.io/pypi/wheel/trading_ig.svg\n    :target: https://pypi.python.org/pypi/trading_ig/\n    :alt: Wheel format\n\n.. image:: https://img.shields.io/pypi/l/trading_ig.svg\n    :target: https://pypi.python.org/pypi/trading_ig/\n    :alt: License\n\n.. image:: https://img.shields.io/pypi/status/trading_ig.svg\n    :target: https://pypi.python.org/pypi/trading_ig/\n    :alt: Development Status\n\n.. image:: https://img.shields.io/pypi/dm/trading_ig.svg\n    :target: https://pypi.python.org/pypi/trading_ig/\n    :alt: Downloads monthly\n\n.. image:: https://requires.io/github/ig-python/ig-markets-api-python-library/requirements.svg?branch=master\n    :target: https://requires.io/github/ig-python/ig-markets-api-python-library/requirements/?branch=master\n    :alt: Requirements Status\n\n.. image:: https://readthedocs.org/projects/trading-ig/badge/?version=latest\n    :target: https://trading-ig.readthedocs.io/en/latest/?badge=latest\n    :alt: Documentation Status\n\ntrading_ig\n==========\n\nA lightweight wrapper for the IG Markets API written in Python. Simplifies access to the IG REST and Streaming APIs\nwith a live or demo account.\n\nWhat is it?\n-----------\n\n`IG Markets <https://www.ig.com/>`_ provides financial spread betting and CFD platforms for trading equities, forex,\ncommodities, indices, cryptocurrencies, bonds, rates, options and more.\n\nIG provide APIs so that developers can access their platforms programmatically. Using the APIs you can\nget live and historical data, automate your trades, or create apps. For details about the IG APIs please see their site:\n\nhttps://labs.ig.com/\n\nNOTE: this is not an IG project. Use it at your own risk\n\nInstallation\n------------\n\nFrom `Python package index <https://pypi.org/project/trading_ig/>`_::\n\n    $ pip install trading_ig\n\nwith `Poetry <https://python-poetry.org/>`_::\n\n    $ git clone https://github.com/ig-python/ig-markets-api-python-library\n    $ cd ig-markets-api-python-library\n    $ poetry install\n\nor with optional packages::\n\n    $ poetry install --extras "pandas munch"\n\nFrom source::\n\n    $ git clone https://github.com/ig-python/ig-markets-api-python-library\n    $ cd ig-markets-api-python-library\n    $ python setup.py install\n\nor direct from Github::\n\n    $ pip install git+https://github.com/ig-python/ig-markets-api-python-library\n\nDependencies\n------------\n\n* `requests <https://pypi.org/project/requests/>`_\n* `pycryptodome <https://pypi.org/project/pycryptodome/>`_\n\nFor full details, see `pyproject.toml <https://github.com/ig-python/ig-markets-api-python-library/blob/master/pyproject.toml>`_\n\nDocs\n----\n\n`<https://trading_ig.readthedocs.io/>`_\n\nLicense\n-------\n\nBSD (See `LICENSE <https://github.com/ig-python/ig-markets-api-python-library/blob/master/LICENSE>`_)\n\n',
    'author': 'Femto Trader',
    'author_email': 'femto.trader@gmail.com',
    'maintainer': 'Andy Geach',
    'maintainer_email': 'andy@bugorfeature.net',
    'url': 'https://github.com/ig-python/ig-markets-api-python-library',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
