# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mecha', 'mecha.resources']

package_data = \
{'': ['*']}

install_requires = \
['beet>=0.36.0', 'tokenstream>=0.6.2']

setup_kwargs = {
    'name': 'mecha',
    'version': '0.2.0',
    'description': 'A powerful Minecraft command library',
    'long_description': '<img align="right" src="https://raw.githubusercontent.com/vberlier/mecha/main/logo.png" alt="logo" width="76">\n\n# Mecha\n\n[![GitHub Actions](https://github.com/vberlier/mecha/workflows/CI/badge.svg)](https://github.com/vberlier/mecha/actions)\n[![PyPI](https://img.shields.io/pypi/v/mecha.svg)](https://pypi.org/project/mecha/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mecha.svg)](https://pypi.org/project/mecha/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\n> A powerful Minecraft command library.\n\n## Introduction\n\nThis package provides a versatile API for generating Minecraft commands in Python. It uses the [`beet`](https://github.com/vberlier/beet) library to generate functions and integrates natively with the `beet` pipeline.\n\n```python\nfrom beet import Context\nfrom mecha import Mecha\n\ndef my_plugin(ctx: Context):\n    mc = ctx.inject(Mecha)\n\n    with mc.function("foo"):\n        mc.say("hello")\n```\n\nYou can directly create handles from data pack instances. The library can be used on its own without being part of a `beet` pipeline.\n\n```python\nfrom beet import DataPack\nfrom mecha import Mecha\n\nwith DataPack(path="demo") as data:\n    mc = Mecha(data)\n\n    with mc.function("foo"):\n        mc.say("hello")\n```\n\n## Installation\n\nThe package can be installed with `pip`.\n\n```bash\n$ pip install mecha\n```\n\n## Contributing\n\nContributions are welcome. Make sure to first open an issue discussing the problem or the new feature before creating a pull request. The project uses [`poetry`](https://python-poetry.org/).\n\n```bash\n$ poetry install\n```\n\nYou can run the tests with `poetry run pytest`.\n\n```bash\n$ poetry run pytest\n```\n\nThe project must type-check with [`pyright`](https://github.com/microsoft/pyright). If you\'re using VSCode the [`pylance`](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) extension should report diagnostics automatically. You can also install the type-checker locally with `npm install` and run it from the command-line.\n\n```bash\n$ npm run watch\n$ npm run check\n```\n\nThe code follows the [`black`](https://github.com/psf/black) code style. Import statements are sorted with [`isort`](https://pycqa.github.io/isort/).\n\n```bash\n$ poetry run isort mecha tests\n$ poetry run black mecha tests\n$ poetry run black --check mecha tests\n```\n\n---\n\nLicense - [MIT](https://github.com/vberlier/mecha/blob/main/LICENSE)\n',
    'author': 'Valentin Berlier',
    'author_email': 'berlier.v@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vberlier/mecha',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
