class ImageprobeError(Exception):
    """Generic base error"""


class CorruptedImage(ImageprobeError):
    """Parsing error"""


class DownloadError(ImageprobeError):
    """Download error

    Attributes:
        url (str): Image URL.
        bytes_read (str): Nr. of bytes received up to the exception raise.
    """

    def __init__(self, url: str, bytes_read: int) -> None:
        self.url = url
        self.bytes_read = bytes_read
        message = f'url: "{url}", {bytes_read} bytes read'
        super().__init__(message)


class UnsupportedFormat(ImageprobeError):
    """Filetype is not supported."""
