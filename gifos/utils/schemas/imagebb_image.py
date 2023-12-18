from dataclasses import dataclass


@dataclass
class ImgbbImage:
    """A class to represent an image uploaded to ImgBB.

    This class represents an image uploaded to ImgBB.

    Attributes:
        id: A string that represents the image's ID on ImgBB.
        url: A string that represents the image's URL on ImgBB.
        delete_url: A string that represents the URL to delete the image from ImgBB.
        file_name: A string that represents the name of the image file.
        expiration: A string that represents the expiration time of the image.
        size: A string that represents the size of the image.
        mime: A string that represents the MIME type of the image.
        extension: A string that represents the extension of the image file.
    """

    __slots__ = [
        "id",
        "url",
        "delete_url",
        "file_name",
        "expiration",
        "size",
        "mime",
        "extension",
    ]
    id: str
    url: str
    delete_url: str
    file_name: str
    expiration: str
    size: str
    mime: str
    extension: str
