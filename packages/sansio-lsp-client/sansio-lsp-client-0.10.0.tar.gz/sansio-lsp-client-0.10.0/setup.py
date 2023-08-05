# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sansio_lsp_client']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.7.3,<2.0.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.7,<0.8']}

setup_kwargs = {
    'name': 'sansio-lsp-client',
    'version': '0.10.0',
    'description': 'An implementation of the client side of the LSP protocol, useful for embedding easily in your editor.',
    'long_description': '# sansio-lsp-client\n\nAn implementation of the client side of the LSP protocol, useful for embedding\neasily in your editor.\n\n\n## Developing\n\n    $ git clone https://github.com/PurpleMyst/sansio-lsp-client\n    $ cd sansio-lsp-client\n    $ python3 -m venv env\n    $ source env/bin/activate\n    (env)$ pip install --upgrade pip\n    (env)$ pip install poetry\n    (env)$ poetry install\n\nMost tests don\'t work on Windows,\nbut GitHub Actions runs tests of all pull requests and uploads coverage files from them.\nTODO: add instructions for looking at coverage files on Windows\n\nTo run tests, first download the langservers you need.\nYou can mostly read `.github/workflows/test.yml`, but the Go langserver is a bit of a gotcha.\nYou will need to install go from https://golang.org/,\nbecause the one from `sudo apt install golang` is too old.\nExtract it inside where you cloned `sansio-lsp-client`\nso that you get an executable named `sansio-lsp-client/go/bin/go`.\n\n    $ tar xf ~/Downloads/go1.16.5.linux-amd64.tar.gz\n\nOnce you have installed all langservers you want, you can run the tests:\n\n    (env)$ PATH="$PATH:$(pwd)/go/bin" poetry run pytest -v\n',
    'author': 'Purple Myst',
    'author_email': 'PurpleMyst@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/PurpleMyst/sansio-lsp-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
