from dataclasses import dataclass


@dataclass(frozen=True)
class ImageData:
    """Contains image metadata.

    Attributes:
        width (int): Width expressed in `w_units`.
        height (int): Height expressed in `h_units`.
        extension (str): File extension, i.e. "png".
        mime_type (str): Mime type, i.e. "image/png".
        w_units (str): Measurement units for `width`. Defaults to "px".
        h_units (str): Measurement units for `height`. Defaults to "px".
    """

    width: int
    height: int
    extension: str
    mime_type: str
    w_units: str = "px"
    h_units: str = "px"
