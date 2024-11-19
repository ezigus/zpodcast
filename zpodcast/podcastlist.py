from zpodcast.podcastdata import PodcastData
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class PodcastList:
    _podcasts: List[PodcastData]

    def __init__(self, podcasts: List[PodcastData] = None) -> None:
        if not isinstance(podcasts, list):
            raise ValueError("Value must be a list")    
        self._podcasts = podcasts if podcasts is not None else []

    def add_podcast(self, podcast: PodcastData) -> None:
        self._podcasts.append(podcast)
            

    def remove_podcast(self, podcast: PodcastData) -> None:
        self._podcasts.remove(podcast)

    def get_all_podcasts(self) -> List[PodcastData]:
        return self._podcasts

    def get_podcast(self, index: int) -> PodcastData:
        if not isinstance(index, int):
            raise ValueError("Non-integer index")
        
        if index < 0:
            raise ValueError("Index less than 0")
        
        if index >= len(self._podcasts):
            raise ValueError("Index greater than size of list")
            
        return self._podcasts[index]