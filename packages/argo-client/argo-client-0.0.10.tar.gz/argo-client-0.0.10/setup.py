# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['argo_client']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0', 'urllib3>=1.26.5']

setup_kwargs = {
    'name': 'argo-client',
    'version': '0.0.10',
    'description': 'A JSON RPC client library.',
    'long_description': '# Argo Client\n\nA python library for client connections to [JSON RPC](https://www.jsonrpc.org/specification) servers, specifically designed with the Haskell [Argo](https://github.com/galoisinc/argo) sister library in mind.\n',
    'author': 'Galois, Inc.',
    'author_email': 'cryptol-team@galois.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4',
}


setup(**setup_kwargs)
