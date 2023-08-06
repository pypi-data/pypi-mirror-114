import struct
from typing import Optional

from imageprobe.client import DownloadClient
from imageprobe.errors import CorruptedImage
from imageprobe.types import ImageData


async def png(client: DownloadClient) -> Optional[ImageData]:
    # Validate PNG signature
    await client.read_from_start(8)
    if not client.buffer.startswith(b"\211PNG\r\n\032\n"):
        return None

    # Check that IHDR chunk exists
    await client.read_from_start(16)
    if client.buffer[12:16] != b"IHDR":
        raise CorruptedImage("Invalid PNG file: missing IHDR chunk")

    # Load IHDR chunk and unpack image metadata
    await client.read_from_start(24)
    try:
        width, height = struct.unpack(">LL", client.buffer[16:24])
    except struct.error as exc:
        raise CorruptedImage("Invalid PNG file: corrupted IHDR chunk") from exc

    return ImageData(
        width=width,
        height=height,
        extension="png",
        mime_type="image/png",
    )
