from dataclasses import dataclass
from typing import List, Dict
from zpodcast.podcastepisodelist import PodcastEpisodeList

@dataclass
class PodcastPlaylist:
    playlists: List[PodcastEpisodeList]

    def add_playlist(self, playlist: PodcastEpisodeList) -> None:
        self.playlists.append(playlist)

    def remove_playlist(self, index: int) -> None:
        del self.playlists[index]

    def get_playlist(self, index: int) -> PodcastEpisodeList:
        return self.playlists[index]

    def get_all_playlists(self) -> List[PodcastEpisodeList]:
        return self.playlists

    def to_dict(self) -> Dict[str, List[Dict]]:
        return {
            "playlists": [playlist.to_dict() for playlist in self.playlists]
        }

    @classmethod
    def from_dict(cls, data: Dict[str, List[Dict]]) -> 'PodcastPlaylist':
        playlists_data = data.get("playlists", [])
        playlists = [PodcastEpisodeList.from_dict(playlist_data) for playlist_data in playlists_data]
        return cls(playlists=playlists)
