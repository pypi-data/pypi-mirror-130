from deezer.client import Client
from deezer.resources import (
    Album,
    Artist,
    Genre,
    Playlist,
    Radio,
    Resource,
    Track,
    User,
)

__version__ = "4.2.1"
__all__ = [
    "Client",
    "Resource",
    "Album",
    "Artist",
    "Genre",
    "Playlist",
    "Track",
    "User",
    "Radio",
]

USER_AGENT = f"Deezer Python API Wrapper v{__version__}"
