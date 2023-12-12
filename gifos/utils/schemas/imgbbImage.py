from dataclasses import dataclass


@dataclass
class imgbbImage:
    __slots__ = [
        "id",
        "url",
        "deleteUrl",
        "fileName",
        "expiration",
        "size",
        "mime",
        "extension",
    ]
    id: str
    url: str
    deleteUrl: str
    fileName: str
    expiration: str
    size: str
    mime: str
    extension: str
