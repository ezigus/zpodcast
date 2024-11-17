from dataclasses import dataclass
import re
from typing import List
#from zpodcast.opmlparser import OPMLParser
#from zpodcast.rsspodcastparser import RSSPodcastParser
from zpodcast.podcastepisode import PodcastEpisode
from typing import Dict

@dataclass
class PodcastPlaylist:
    name: str
    episodes: List[PodcastEpisode]
    
    def __post_init__(self):
        self._validate_name(self.name)
    
    def set_name(self, name: str) -> None:
        self._validate_name(name)
        self.name = name
    
    def _validate_name(self, name: str) -> None:
        print(f"name = {name}")
        if not bool(re.match('([a-zA-Z0-9\s]+$)', name)):
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
            total_duration_seconds = episode.duration_in_seconds
        return total_duration_seconds

    def _format_duration(self, duration_seconds: float) -> str:
        days = int(duration_seconds // 86400)
        hours = int((duration_seconds % 86400) // 3600)
        minutes = int((duration_seconds % 3600) // 60)
        seconds = int(duration_seconds % 60)
        return f"{days} days, {hours:02d}:{minutes:02d}:{seconds:02d}"

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
