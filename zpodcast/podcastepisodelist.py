from dataclasses import dataclass
import re
from typing import List
from zpodcast.podcastepisode import PodcastEpisode
from typing import Dict

@dataclass
class PodcastEpisodeList:
    _name: str
    _episodes: List[PodcastEpisode]
    
    def __init__(self,
                 name : str,
                 episodes : List[PodcastEpisode]
                 ):
        self.name = name
        self.episodes = episodes
        
    def __post_init__(self):
        self._validate_name(self._name)
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name: str) -> None:
        self._validate_name(name)
        self._name = name
    
    def _validate_name(self, name: str) -> None:
        if not isinstance(name, str):
            raise ValueError("Invalid playlist name. Playlist name is not a string.")

        if not bool(re.match('([a-zA-Z0-9\ ]+$)', name)):
            raise ValueError("Invalid playlist name. The name must be alphanumeric.")
        
        if len(name) > 100:
            raise ValueError(f"Invalid playlist name. The name is {len(name)} and the maximum length is 100 characters.")
    
    @property
    def episodes(self):
        return self._episodes
    
    @episodes.setter
    def episodes(self, episodes: List[PodcastEpisode]):
        self._episodes = episodes
        
        
    def add_podcastepisode(self, episode: PodcastEpisode) -> None:
        self._episodes.append(episode)

    def remove_podcastepisode(self, index: int) -> None:
        del self._episodes[index]

    def get_num_items(self) -> int:
        return len(self._episodes)

    def calculate_duration(self) -> float:
        total_duration_seconds = 0.0
        for episode in self._episodes:
            total_duration_seconds += episode.duration
        return total_duration_seconds

    def _format_duration(self, duration_seconds: float) -> str:
        days = int(duration_seconds // 86400)
        hours = int((duration_seconds % 86400) // 3600)
        minutes = int((duration_seconds % 3600) // 60)
        seconds = int(duration_seconds % 60)
        string = f"{days} days, {hours:02d}:{minutes:02d}:{seconds:02d}"
        return string

    def convert_duration_to_string(self, duration_seconds: float) -> str:
        return self._format_duration(duration_seconds)

    def move_episode_up(self, index: int) -> None:
        if index > 0 and index < len(self._episodes):
            self._episodes[index], self._episodes[index - 1] = self._episodes[index - 1], self._episodes[index]

    def move_episode_down(self, index: int) -> None:
        if index >= 0 and index < len(self._episodes) - 1:
            self._episodes[index], self._episodes[index + 1] = self._episodes[index + 1], self._episodes[index]

    def move_episode_to_position(self, current_index: int, new_index: int) -> None:
        if current_index >= 0 and current_index < len(self._episodes) and new_index >= 0 and new_index < len(self._episodes):
            episode = self._episodes.pop(current_index)
            self._episodes.insert(new_index, episode)

    def get_all_episode_details(self) -> List[Dict[str, str]]:
        episode_details = []
        for episode in self._episodes:
            details = {
                "title": episode.title,
                "duration": episode.duration,
                "audio_url": episode.audio_url
            }
            episode_details.append(details)
        return episode_details

    def get_episode_details(self, index: int) -> Dict[str, str]:
        if index < 0 or index >= len(self._episodes):
            return {}
        episode = self._episodes[index]
        return {
            "title": episode.title,
            "duration": episode.duration,
            "audio_url": episode.audio_url
        }

    """
    if the passed indices list is not entered or is none, then get all of the episodes.
    """
    def get_episodes(self, indices: List[int] = None) -> List[PodcastEpisode]:
        if indices is None:
            return self._episodes
        
        valid_indices = [i for i in indices if isinstance(i, int) and 0 <= i < len(self._episodes)]
        if len(valid_indices) != len(indices):
            raise ValueError("Invalid indices provided.")
        return [self._episodes[i] for i in valid_indices]

    @classmethod
    def from_dict(cls, data: Dict[str, any]) -> 'PodcastEpisodeList':
        mandatory_keys = ['name', 'episodes']
        for key in mandatory_keys:
            if key not in data:
                raise ValueError(f"Missing mandatory key: {key}")
        
        name = data.get("name")
        episodes_data = data.get("episodes")
        
        episodes = []
        for episode_data in episodes_data:
            try:
                episode = PodcastEpisode(title = episode_data.get("title"),
                                         audio_url=episode_data.get("audio_url"),
                                         description = episode_data.get("description"),
                                         pub_date = episode_data.get("pub_date"),
                                         duration = episode_data.get("duration"),
                                         episode_number = episode_data.get("episode_number"),
                                         image_url = episode_data.get("image_url"),
                                         )
                episodes.append(episode)
            except TypeError as e:
                raise ValueError(f"Invalid episode data: {e}")
            
        podcastepisodelist = PodcastEpisodeList(name = name, episodes = episodes)
        return podcastepisodelist

    def to_dict(self) -> Dict:
        podcastepisodelist_dict = {
            "name": self.name,
            "episodes": [episode.to_dict() for episode in self.episodes]
            }
        return podcastepisodelist_dict
        
