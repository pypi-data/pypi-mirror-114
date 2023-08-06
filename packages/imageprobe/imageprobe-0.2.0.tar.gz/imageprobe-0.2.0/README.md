# imageprobe

[![Latest PyPI package version](https://img.shields.io/pypi/v/imageprobe.svg)](https://pypi.org/project/imageprobe)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/imageprobe.svg)](https://pypi.org/project/imageprobe)
[![Development status](https://img.shields.io/pypi/status/imageprobe)](https://pypi.org/project/imageprobe)
[![CI](https://github.com/palt0/imageprobe/workflows/CI/badge.svg)](https://github.com/palt0/imageprobe/actions?query=workflow%3ACI)
[![Codecov](https://codecov.io/gh/palt0/imageprobe/branch/main/graph/badge.svg?token=DIHQIYQJ91)](https://codecov.io/gh/palt0/imageprobe)

Asynchronous library to get image dimensions by fetching as little data as possible.

It temporarily supports only GIF, PNG because development is still in a very early stage.

## Usage

To install this library, run:

    pip install imageprobe

The `probe()` function returns metadata of an image from an URL, or throws an exception if an error occurred.

```python
import asyncio
from imageprobe import probe

loop = asyncio.get_event_loop()
url = "https://upload.wikimedia.org/wikipedia/commons/7/70/Example.png"
image_data = loop.run_until_complete(probe(url))
print(image_data.width, image_data.height)

# 172 178
```

Under the hood, `probe()` creates an `aiohttp.ClientSession`, but you can pass a pre-existing session as an optional argument if you prefer.

## Contributing

I won't accept pull requests until the first beta release.
