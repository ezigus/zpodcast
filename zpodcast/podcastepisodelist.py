from dataclasses import dataclass
import re
from typing import List
from zpodcast.podcastepisode import PodcastEpisode
from typing import Dict

@dataclass
class PodcastEpisodeList:
    name: str
    episodes: List[PodcastEpisode]
    
    def __post_init__(self):
        self._validate_name(self.name)
    
    def set_name(self, name: str) -> None:
        self._validate_name(name)
        self.name = name
    
    def _validate_name(self, name: str) -> None:
        if not isinstance(name, str):
            raise ValueError("Invalid playlist name. Playlist name is not a string.")

        if not bool(re.match('([a-zA-Z0-9\ ]+$)', name)):
            raise ValueError("Invalid playlist name. The name must be alphanumeric.")
        
        if len(name) > 100:
            raise ValueError(f"Invalid playlist name. The name is {len(name)} and the maximum length is 100 characters.")
        
    def add_podcastepisode(self, episode: PodcastEpisode) -> None:
        self.episodes.append(episode)

    def remove_podcastepisode(self, index: int) -> None:
        del self.episodes[index]

    def get_num_items(self) -> int:
        return len(self.episodes)

    def calculate_duration(self) -> float:
        total_duration_seconds = 0.0
        for episode in self.episodes:
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
        if index > 0 and index < len(self.episodes):
            self.episodes[index], self.episodes[index - 1] = self.episodes[index - 1], self.episodes[index]

    def move_episode_down(self, index: int) -> None:
        if index >= 0 and index < len(self.episodes) - 1:
            self.episodes[index], self.episodes[index + 1] = self.episodes[index + 1], self.episodes[index]

    def move_episode_to_position(self, current_index: int, new_index: int) -> None:
        if current_index >= 0 and current_index < len(self.episodes) and new_index >= 0 and new_index < len(self.episodes):
            episode = self.episodes.pop(current_index)
            self.episodes.insert(new_index, episode)

    def get_all_episode_details(self) -> List[Dict[str, str]]:
        episode_details = []
        for episode in self.episodes:
            details = {
                "title": episode.title,
                "duration": episode.duration,
                "audio_url": episode.audio_url
            }
            episode_details.append(details)
        return episode_details

    def get_episode_details(self, index: int) -> Dict[str, str]:
        if index < 0 or index >= len(self.episodes):
            return {}
        episode = self.episodes[index]
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
            return self.episodes
        
        valid_indices = [i for i in indices if isinstance(i, int) and 0 <= i < len(self.episodes)]
        if len(valid_indices) != len(indices):
            raise ValueError("Invalid indices provided.")
        return [self.episodes[i] for i in valid_indices]

    @classmethod
    def from_dict(cls, data: Dict[str, any]) -> 'PodcastEpisodeList':
        mandatory_keys = ['name', 'episodes']
        for key in mandatory_keys:
            if key not in data:
                raise ValueError(f"Missing mandatory key: {key}")
        
        name = data['name']
        episodes_data = data['episodes']
        
        episodes = []
        for episode_data in episodes_data:
            try:
                episode = PodcastEpisode(**episode_data)
                episodes.append(episode)
            except TypeError as e:
                raise ValueError(f"Invalid episode data: {e}")
                
        return cls(name=name, episodes=episodes)

    def to_dict(self) -> Dict[str, any]:
        return {
            "name": self.name,
            "episodes": [episode.to_dict() for episode in self.episodes]
        }
