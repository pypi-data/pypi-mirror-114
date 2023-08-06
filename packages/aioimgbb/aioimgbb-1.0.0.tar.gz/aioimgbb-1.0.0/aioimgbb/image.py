from dataclasses import dataclass


@dataclass
class Image:
    id: str
    title: str
    url_viewer: str
    url: str
    display_url: str
    size: str
    time: str
    expiration: str