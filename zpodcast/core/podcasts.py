from dataclasses import dataclass
from typing import List, Dict, Any, Union
from zpodcast.core.podcast import PodcastData

@dataclass
class PodcastList:
    _podcasts: List[PodcastData]
    _instance = None

    def __init__(self, podcasts: List[PodcastData] = []) -> None:
        if not isinstance(podcasts, list):
            raise ValueError("Value must be a list")    

        self._podcasts = podcasts 

    @classmethod
    def get_instance(cls) -> 'PodcastList':
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @property
    def podcasts(self):
        return self._podcasts
    
    @podcasts.setter
    def podcasts(self,
                 podcasts: List[PodcastData]):
        if not isinstance(podcasts, list):
            raise ValueError("Value must be a list")    
        self._podcasts = podcasts


    def add_podcast(self, podcast: PodcastData) -> PodcastData:
        self._podcasts.append(podcast)
        return podcast
            

    def remove_podcast(self, podcast: PodcastData) -> None:
        self._podcasts.remove(podcast)

    def get_podcast(self, index: int) -> PodcastData:
        if not isinstance(index, int):
            raise ValueError("Non-integer index")
        
        if index < 0:
            raise ValueError("Index less than 0")
        
        if index >= len(self._podcasts):
            raise ValueError("Index greater than size of list")
            
        return self._podcasts[index]

    def delete_podcast(self, index: int) -> None:
        """Delete a podcast by its index"""
        if not isinstance(index, int):
            raise ValueError("Non-integer index")

        if index < 0 or index >= len(self._podcasts):
            raise ValueError("Index out of range")

        del self._podcasts[index]

    def update_podcast(self, index: Union[int, str], data: Dict[str, Any]) -> PodcastData:
        """
        Update a podcast with new data
        
        Args:
            index (Union[int, str]): The index of the podcast to update
            data (Dict[str, Any]): Dictionary containing podcast attributes to update
            
        Returns:
            PodcastData: The updated podcast
            
        Raises:
            ValueError: If index is invalid or podcast is not found
        """
        # Convert string index to int if needed
        if isinstance(index, str):
            try:
                index = int(index)
            except ValueError:
                raise ValueError("Invalid podcast index")

        # Validate index
        if not isinstance(index, int) or index < 0 or index >= len(self._podcasts):
            raise ValueError("Podcast not found")
            
        # Get the podcast to update
        podcast = self._podcasts[index]
        
        # Check if podcast_url is being updated
        url_update = 'podcast_url' in data and data['podcast_url'] != podcast.podcast_url
        
        # Update allowed attributes
        if 'title' in data:
            podcast.title = data['title']
        if 'host' in data:
            podcast.host = data['host']
        if 'description' in data:
            podcast.description = data['description']
        if 'podcast_priority' in data:
            podcast.podcast_priority = data['podcast_priority']
        if 'image_url' in data:
            podcast.image_url = data['image_url']
        if url_update:
            # Only update URL and re-populate if it's actually changed
            podcast.podcast_url = data['podcast_url']
            # Prevent automatic population by setting name_set_manually
            podcast.name_set_manually = True
            # Manually trigger episode refresh
            podcast.populate_episodes_from_feed()
            
        return podcast

    def to_dict(self):
        return {
            "podcasts": [podcast.to_dict() for podcast in self._podcasts]
        }

    @classmethod
    def from_dict(cls, data):
        podcasts_data = data.get("podcasts", [])
        podcasts = [PodcastData.from_dict(podcast_data) for podcast_data in podcasts_data]
        return cls(podcasts=podcasts)
