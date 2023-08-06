# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['imageprobe', 'imageprobe.parsers']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.3,<4.0.0']

extras_require = \
{':python_version >= "3.6.2" and python_version < "3.7.0"': ['dataclasses>=0.7,<0.8']}

setup_kwargs = {
    'name': 'imageprobe',
    'version': '0.2.0',
    'description': 'Asynchronous image probing library. Fetch only as much as you need!',
    'long_description': '# imageprobe\n\n[![Latest PyPI package version](https://img.shields.io/pypi/v/imageprobe.svg)](https://pypi.org/project/imageprobe)\n[![Supported Python versions](https://img.shields.io/pypi/pyversions/imageprobe.svg)](https://pypi.org/project/imageprobe)\n[![Development status](https://img.shields.io/pypi/status/imageprobe)](https://pypi.org/project/imageprobe)\n[![CI](https://github.com/palt0/imageprobe/workflows/CI/badge.svg)](https://github.com/palt0/imageprobe/actions?query=workflow%3ACI)\n[![Codecov](https://codecov.io/gh/palt0/imageprobe/branch/main/graph/badge.svg?token=DIHQIYQJ91)](https://codecov.io/gh/palt0/imageprobe)\n\nAsynchronous library to get image dimensions by fetching as little data as possible.\n\nIt temporarily supports only GIF, PNG because development is still in a very early stage.\n\n## Usage\n\nTo install this library, run:\n\n    pip install imageprobe\n\nThe `probe()` function returns metadata of an image from an URL, or throws an exception if an error occurred.\n\n```python\nimport asyncio\nfrom imageprobe import probe\n\nloop = asyncio.get_event_loop()\nurl = "https://upload.wikimedia.org/wikipedia/commons/7/70/Example.png"\nimage_data = loop.run_until_complete(probe(url))\nprint(image_data.width, image_data.height)\n\n# 172 178\n```\n\nUnder the hood, `probe()` creates an `aiohttp.ClientSession`, but you can pass a pre-existing session as an optional argument if you prefer.\n\n## Contributing\n\nI won\'t accept pull requests until the first beta release.\n',
    'author': 'Plato',
    'author_email': 'platoo@outlook.it',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://github.com/palt0/imageprobe',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<3.10',
}


setup(**setup_kwargs)
