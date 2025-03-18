from dataclasses import dataclass
from typing import List
from zpodcast.core.podcast import PodcastData

@dataclass
class PodcastList:
    _podcasts: List[PodcastData]

    def __init__(self, podcasts: List[PodcastData] = []) -> None:
        if not isinstance(podcasts, list):
            raise ValueError("Value must be a list")    

        self._podcasts = podcasts 

    @property
    def podcasts(self):
        return self._podcasts
    
    @podcasts.setter
    def podcasts(self,
                 podcasts: List[PodcastData]):
        if not isinstance(podcasts, list):
            raise ValueError("Value must be a list")    
        self._podcasts = podcasts


    def add_podcast(self, podcast: PodcastData) -> None:
        self._podcasts.append(podcast)
            

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

    def to_dict(self):
        return {
            "podcasts": [podcast.to_dict() for podcast in self._podcasts]
        }

    @classmethod
    def from_dict(cls, data):
        podcasts_data = data.get("podcasts", [])
        podcasts = [PodcastData.from_dict(podcast_data) for podcast_data in podcasts_data]
        return cls(podcasts=podcasts)
