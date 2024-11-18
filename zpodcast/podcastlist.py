from zpodcast.podcastdata import PodcastData
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class PodcastList:
    _podcasts: Optional[List[PodcastData]]

    def __init__(self, podcasts: List[PodcastData] = None) -> None:
        self._podcasts = podcasts if podcasts is not None else []

    def add_podcast(self, podcast: PodcastData) -> None:
        self._podcasts.append(podcast)

    def remove_podcast(self, podcast: PodcastData) -> None:
        self._podcasts.remove(podcast)

    def insert_podcast(self, index: int, podcast: PodcastData) -> None:
        self._podcasts.insert(index, podcast)

    def get_all_podcasts(self) -> List[PodcastData]:
        return self._podcasts

    def get_podcast(self, index: int) -> PodcastData:
        if not isinstance(index, int) or index < 0 or index >= len(self._podcasts):
            raise ValueError("Invalid index")
        return self._podcasts[index]
