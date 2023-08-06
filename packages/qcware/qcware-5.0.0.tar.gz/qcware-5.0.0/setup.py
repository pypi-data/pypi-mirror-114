# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qcware',
 'qcware.forge',
 'qcware.forge.api_calls',
 'qcware.forge.circuits',
 'qcware.forge.circuits.api',
 'qcware.forge.config',
 'qcware.forge.optimization',
 'qcware.forge.optimization.api',
 'qcware.forge.qio',
 'qcware.forge.qio.api',
 'qcware.forge.qml',
 'qcware.forge.qml.api',
 'qcware.forge.qutils',
 'qcware.forge.qutils.api',
 'qcware.forge.test',
 'qcware.forge.test.api',
 'qcware.serialization',
 'qcware.serialization.transforms',
 'qcware.types',
 'qcware.types.optimization',
 'qcware.types.optimization.problem_spec',
 'qcware.types.optimization.problem_spec.utils',
 'qcware.types.optimization.results',
 'qcware.types.optimization.results.utils',
 'qcware.types.optimization.utils']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.4.post0',
 'backoff>=1.10.0',
 'colorama>=0.4.4',
 'icontract>=2.5.3',
 'lz4>=3.1.3',
 'networkx>=2.5.1',
 'numpy>=1.21.0',
 'packaging>=20.9',
 'pydantic>=1.8.2',
 'python-decouple>=3.4',
 'qcware-quasar>=1.0.3',
 'qubovert>=1.2.3',
 'requests>=2.25.1',
 'setuptools>=57.1.0',
 'tabulate>=0.8.9']

setup_kwargs = {
    'name': 'qcware',
    'version': '5.0.0',
    'description': "The python client for QC Ware's Forge SaaS quantum computing product",
    'long_description': '\n\n.. image:: http://qcwareco.wpengine.com/wp-content/uploads/2019/08/qc-ware-logo-11.png\n   :target: http://qcwareco.wpengine.com/wp-content/uploads/2019/08/qc-ware-logo-11.png\n   :alt: logo\n\n\nQC Ware Platform Client Library (Python)\n========================================\n\nThis package contains functions for easily interfacing with the QC Ware\nPlatform from Python.\n\n\n.. image:: https://badge.fury.io/py/qcware.svg\n   :target: https://badge.fury.io/py/qcware\n   :alt: PyPI version\n\n.. image:: https://pepy.tech/badge/qcware\n   :target: https://pepy.tech/project/qcware\n   :alt: Downloads\n\n.. image:: https://pepy.tech/badge/qcware/month\n   :target: https://pepy.tech/project/qcware/month\n   :alt: Downloads\n\n.. image:: https://circleci.com/gh/qcware/platform_client_library_python.svg?style=svg\n   :target: https://circleci.com/gh/qcware/platform_client_library_python\n   :alt: CircleCI\n\n.. image:: https://readthedocs.org/projects/qcware/badge/?version=latest\n   :target: https://qcware.readthedocs.io/en/latest/?badge=latest\n   :alt: Documentation Status\n\n\nInstallation\n____________\n\nThis documentation is for the latest (prerelease) version of QCWare\'s Forge client, which\nat present relies on some internal packages.  It is "baked into" QCWare\'s Jupyterhub\nnotebooks, but local installation will have to wait until Quasar, our circuit-model\nlibrary, is publicly available.\n\nOrdinarily, you would install as follows:\n\nTo install with pip:\n\n.. code:: shell\n\n   pip install qcware\n\nOr, to install from source:\n\n.. code:: shell\n\n   git clone https://github.com/qcware/platform_client_library_python.git\n   cd platform_client_library_python\n   pip install -e .\n\nSign up for an API key at `https://forge.qcware.com <https://forge.qcware.com>`_ to access *Forge*. Please see our `documentation <https://qcware.readthedocs.io>`_.\n\nPlease see the `documentation <https://qcware.readthedocs.io>`_\n',
    'author': 'Vic Putz',
    'author_email': 'vic.putz@qcware.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://github.com/qcware/platform_client_library_python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
