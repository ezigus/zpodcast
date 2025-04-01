"""
Handles JSON import and export for podcasts and playlists.

This class provides static methods to serialize and deserialize podcast and playlist
data to and from JSON files. It ensures version compatibility and validates the
structure of the JSON data.

Attributes:
    VERSION (str): The version of the JSON format supported by this class.

Methods:
    export_podcast_list(podcast_list: PodcastList, filename: str = None) -> None:
        Exports a PodcastList object to a JSON file.

    import_podcast_list(filename: str) -> PodcastList:
        Imports a PodcastList object from a JSON file.

    export_podcast_playlist(podcast_playlist: PodcastPlaylist, filename: str = None) -> None:
        Exports a PodcastPlaylist object to a JSON file.

    import_podcast_playlist(filename: str) -> PodcastPlaylist:
        Imports a PodcastPlaylist object from a JSON file.

Raises:
    ValueError: If the JSON version is unsupported.
"""

from typing import Optional

import json

from zpodcast.core.podcasts import PodcastList
from zpodcast.core.playlists import PodcastPlaylist


class PodcastJSON:
    VERSION = "0.1"

    @staticmethod
    def export_podcast_list(podcast_list: PodcastList, filename: Optional[str] = None) -> None:
        if filename is None:
            filename = f"PodcastList-{PodcastJSON.VERSION}.json"
        with open(filename, "w") as f:
            json.dump(
                {"version": PodcastJSON.VERSION, "podcastlist": podcast_list.to_dict()},
                f,
                indent=4,
            )

    @staticmethod
    def import_podcast_list(filename: str) -> PodcastList:
        with open(filename, "r") as f:
            data = json.load(f)
            print("Reading podcast_list.json:", data)  # Debugging
            if data.get("version") != PodcastJSON.VERSION:
                raise ValueError("Unsupported version")
            return PodcastList.from_dict(data.get("podcastlist"))

    @staticmethod
    def export_podcast_playlist(
        podcast_playlist: PodcastPlaylist, filename: Optional[str] = None
    ) -> None:
        if filename is None:
            filename = f"PodcastPlaylist-{PodcastJSON.VERSION}.json"
        with open(filename, "w") as f:
            json.dump(
                {
                    "version": PodcastJSON.VERSION,
                    "podcastplaylist": podcast_playlist.to_dict(),
                },
                f,
                indent=4,
            )

    @staticmethod
    def import_podcast_playlist(filename: str) -> PodcastPlaylist:
        with open(filename, "r") as f:
            data = json.load(f)
            if data.get("version") != PodcastJSON.VERSION:
                raise ValueError("Unsupported version")
            return PodcastPlaylist.from_dict(data.get("podcastplaylist"))
