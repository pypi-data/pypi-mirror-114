from typing import Optional

import aiohttp

from imageprobe.client import DownloadClient
from imageprobe.errors import UnsupportedFormat
from imageprobe.parsers import ordered_parsers as parsers
from imageprobe.types import ImageData


async def probe(url: str, session: Optional[aiohttp.ClientSession] = None) -> ImageData:
    """Download as little data as possible to determine the dimensions of an image.

    Args:
        url (str): Image URL.
        session (Optional[aiohttp.ClientSession]): Pre-existing session. Defaults to
            None if you want to instantiate a new one.

    Raises:
        CorruptedImage: Image is corrupted.
        DownloadError: Image wasn't downloaded successfully.
        UnsupportedFormat: Filetype is not supported.

    Returns:
        ImageData: Object containing image metadata.
    """
    async with DownloadClient(url, session) as client:
        _image_data: Optional[ImageData] = None
        for parser in parsers:
            _image_data = await parser(client)
            if _image_data is not None:
                break

        if _image_data is None:
            raise UnsupportedFormat
        return _image_data
