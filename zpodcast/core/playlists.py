"""
This module defines the PodcastPlaylist class, which manages multiple podcast playlists.
It provides methods for adding, removing, and retrieving playlists, as well as serialization.
"""

from dataclasses import dataclass
from typing import List, Dict
from zpodcast.core.playlist import PodcastEpisodeList


@dataclass
class PodcastPlaylist:
    """
    Represents a collection of podcast playlists.

    Attributes:
        playlists (List[PodcastEpisodeList]): A list of podcast playlists.
    """

    _playlists: List[PodcastEpisodeList]
    _instance = None

    def __init__(self, playlists):
        self.playlists = playlists

    @classmethod
    def get_instance(cls) -> "PodcastPlaylist":
        if cls._instance is None:
            cls._instance = cls(playlists=[])
        return cls._instance

    @property
    def playlists(self):
        return self._playlists

    @playlists.setter
    def playlists(self, playlists: List[PodcastEpisodeList]):
        if not isinstance(playlists, list):
            return ValueError("Only settable if this is a list of PodcastEpisodeLists")

        if not playlists == [] and not isinstance(playlists[0], PodcastEpisodeList):
            return ValueError(
                "Only settable if the values in the list are PodcastEpisodeList"
            )

        self._playlists = playlists

    def add_playlist(self, playlist: PodcastEpisodeList) -> None:
        """
        Add a new playlist to the collection.

        Args:
            playlist (PodcastEpisodeList): The playlist to add.
        """
        self.playlists.append(playlist)

    def remove_playlist(self, index: int) -> None:
        del self.playlists[index]

    def get_playlist(self, index: int) -> PodcastEpisodeList:
        return self.playlists[index]

    def get_all_playlists(self) -> List[PodcastEpisodeList]:
        return self.playlists

    def to_dict(self) -> Dict[str, List[Dict]]:
        """
        Serialize the PodcastPlaylist object to a dictionary.

        Returns:
            Dict[str, List[Dict]]: A dictionary representation of the playlist collection.
        """
        return {"playlists": [playlist.to_dict() for playlist in self.playlists]}

    @classmethod
    def from_dict(cls, data: Dict[str, List[Dict]]) -> "PodcastPlaylist":
        playlists_data = data.get("playlists", [])
        playlists = [
            PodcastEpisodeList.from_dict(playlist_data)
            for playlist_data in playlists_data
        ]
        return cls(playlists=playlists)
