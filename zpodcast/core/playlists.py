from dataclasses import dataclass
from typing import List, Dict
from zpodcast.core.playlist import PodcastEpisodeList


@dataclass
class PodcastPlaylist:
    """
    Represents a collection of podcast playlists.

    This class provides functionality to manage multiple playlists of podcast episodes,
    including adding, removing, and retrieving playlists. It also supports serialization
    to and from dictionaries.

    Attributes:
        _playlists (List[PodcastEpisodeList]): A list of podcast playlists.
        _instance (PodcastPlaylist): A singleton instance of the class.

    Methods:
        get_instance() -> PodcastPlaylist:
            Returns the singleton instance of the PodcastPlaylist class.

        add_playlist(playlist: PodcastEpisodeList) -> None:
            Adds a new playlist to the collection.

        remove_playlist(index: int) -> None:
            Removes a playlist from the collection by its index.

        get_playlist(index: int) -> PodcastEpisodeList:
            Retrieves a specific playlist by its index.

        get_all_playlists() -> List[PodcastEpisodeList]:
            Returns all playlists in the collection.

        to_dict() -> Dict[str, List[Dict]]:
            Serializes the PodcastPlaylist object to a dictionary.

        from_dict(data: Dict[str, List[Dict]]) -> PodcastPlaylist:
            Creates a PodcastPlaylist object from a dictionary.

    Raises:
        ValueError: If invalid data is provided for playlists.
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
        self.playlists.append(playlist)

    def remove_playlist(self, index: int) -> None:
        del self.playlists[index]

    def get_playlist(self, index: int) -> PodcastEpisodeList:
        return self.playlists[index]

    def get_all_playlists(self) -> List[PodcastEpisodeList]:
        return self.playlists

    def to_dict(self) -> Dict[str, List[Dict]]:
        return {"playlists": [playlist.to_dict() for playlist in self.playlists]}

    @classmethod
    def from_dict(cls, data: Dict[str, List[Dict]]) -> "PodcastPlaylist":
        playlists_data = data.get("playlists", [])
        playlists = [
            PodcastEpisodeList.from_dict(playlist_data)
            for playlist_data in playlists_data
        ]
        return cls(playlists=playlists)
