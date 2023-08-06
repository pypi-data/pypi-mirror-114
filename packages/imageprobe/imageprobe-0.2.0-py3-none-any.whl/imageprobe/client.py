from types import TracebackType
from typing import Optional, Type

import aiohttp

from imageprobe.errors import DownloadError


class DownloadClient:
    """Wrapper for aiohttp.ClientSession.

    It either creates a new private ClientSession instance or uses a pre-existing one if
    it is provided at inizialization.
    Read methods fail at if EOF is reached before reading enough data.

    Attributes:
        url (str): Image URL.
        buffer (bytes): Bytes downloaded from `url`.
        bytes_read (int): Syntactic sugar for `len(buffer)`.
    """

    def __init__(
        self,
        url: str,
        session: Optional[aiohttp.ClientSession] = None,
    ) -> None:
        self.url = url
        self.buffer = b""
        self._cs: aiohttp.ClientSession
        self._external_cs = session
        self._response: aiohttp.ClientResponse

    @property
    def bytes_read(self) -> int:
        return len(self.buffer)

    async def __aenter__(self) -> "DownloadClient":
        # If no client session is provided, instantiate a new one.
        if self._external_cs is None:
            self._cs = aiohttp.ClientSession()
        else:
            self._cs = self._external_cs

        try:
            self._response = await self._cs.get(self.url)
            return self
        except aiohttp.ClientError as exc:
            if self._external_cs is None:
                await self._cs.close()
            raise DownloadError(self.url, self.bytes_read) from exc

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: TracebackType,
    ) -> None:
        await self._release()

    async def _release(self) -> None:
        """Gracefully interrupts the connection.

        It also closes the client session if it wasn't provided externally.
        """
        await self._response.release()
        if self._external_cs is None:
            await self._cs.close()

    async def read(self, nr_bytes: int) -> None:
        """Reads `nr_bytes` bytes."""
        try:
            old_buflen = self.bytes_read
            self.buffer += await self._response.content.read(nr_bytes)
        except aiohttp.ClientError as exc:
            await self._release()
            raise DownloadError(self.url, self.bytes_read) from exc

        # Differently from classic implementations, we require to read all nr_bytes (and
        # not up to nr_bytes).
        if self.bytes_read - old_buflen < nr_bytes:
            await self._release()
            raise DownloadError(self.url, self.bytes_read)

    async def read_from_start(self, nr_bytes: int) -> None:
        """Reads `nr_bytes` from the beginning of the file."""
        bytes_diff = nr_bytes - self.bytes_read
        if bytes_diff:
            await self.read(bytes_diff)
