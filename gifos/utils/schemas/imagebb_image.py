from dataclasses import dataclass


@dataclass
class ImgbbImage:
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
