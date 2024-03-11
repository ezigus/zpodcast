from dataclasses import dataclass
from typing import List
from opmlparser import OPMLParser
from rsspodcastparser import RSSPodcastParser
from podcastepisode import PodcastEpisode
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
        if not name.isalnum() or len(name) > 100:
            raise ValueError("Invalid playlist name. The name must be alphanumeric and have a maximum length of 100 characters.")
        
    def add_podcast(self, episode: PodcastEpisode) -> None:
        self.episodes.append(episode)

    def remove_podcast(self, index: int) -> None:
        del self.episodes[index]

    def insert_podcast(self, episode: PodcastEpisode, index: int) -> None:
        self.episodes.insert(index, episode)

    def get_num_items(self) -> int:
        return len(self.episodes)

    def calculate_duration(self) -> float:
        total_duration_seconds = 0.0
        for episode in self.episodes:
            total_duration_seconds += episode.duration_in_seconds
        return total_duration_seconds

    def _format_duration(self, duration_seconds: float) -> str:
        days = int(duration_seconds // 86400)
        hours = int((duration_seconds % 86400) // 3600)
        minutes = int((duration_seconds % 3600) // 60)
        seconds = int(duration_seconds % 60)
        return f"{days} days, {hours:02d}:{minutes:02d}:{seconds:02d}"

    def convert_duration_to_string(self, duration_seconds: float) -> str:
        return self._format_duration(duration_seconds)

def main():
    # Create an instance of RSSPlaylist with an empty list of episodes
    playlist: PodcastPlaylist = PodcastPlaylist(name="zPodcastTest", episodes=[])

    # Parse the OPML file and retrieve the RSS feeds
    rss_feeds: List[Dict[str, str]] = OPMLParser.parse_opml_file('test.opml')
    
    if rss_feeds:
        # Get the episodes from the first RSS feed
        episodes: List[PodcastEpisode] = RSSPodcastParser.get_episodes(rss_feeds[0]['url'])
        
        # Sort episodes by publication date in descending order
        episodes.sort(key=lambda episode: episode.pub_date, reverse=True)
        
        # Add the most recent 5 episodes to the playlist
        for episode in episodes[:5]:
            playlist.add_podcast(episode)
        
        # Get the number of items in the playlist
        num_items: int = playlist.get_num_items()
        
        # Calculate the duration of the playlist in seconds
        playlist_duration: float = playlist.calculate_duration()
        
        # Print the number of items in the playlist
        print(f"Number of items in the playlist: {num_items}")
        
        # Print the duration of the playlist in seconds
        print(f"Duration of the playlist: {playlist_duration} seconds")
        
        # Print the duration of the playlist in a formatted string
        print(f"Duration of the playlist: {playlist.convert_duration_to_string(playlist_duration)}")

if __name__ == "__main__":
    main()