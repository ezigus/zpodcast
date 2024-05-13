
from podcastepisode import PodcastEpisode
from dataclasses import dataclass
from typing import Optional, List

"""
    This class manages all types of lists for this application.  
    It stores the list of episodes associated with a podcast
    It stores a list of episodes that make up a podcast
    It allows you to resort the list, by passing in a function or using one of the built in ones that is built into this class
"""
@dataclass
class PodcastList:
    
    _episodes: Optional [List[PodcastEpisode]]
    
    
    def __init__(self, episodes: List[PodcastEpisode]=None) -> None:
        self._episdoes = episodes
        
    def GetFirst(self) -> PodcastEpisode:
        return(self._episodes[0])
    
    def GetLast(self) -> PodcastEpisode:
        return(self._episodes[self._episodes.count-1])
    
    def AddToEnd(self, episode: PodcastEpisode) -> None:
        self._episodes.append(episode)
    
    def RemoveFromEnd(self, episode: PodcastEpisode) -> None:
        self._episodes.pop()
    
    def AddAfter(self, existingEpisode: PodcastEpisode, NewEpisode: PodcastEpisode) -> None:
        pass
    
    def AddBefore(self, existingEpisode: PodcastEpisode) -> None:
        pass
    
    def SortByDateTime(self) -> None:
        pass
    
    def EmptyEpisodeList(self) -> None:
        self._episodes.clear()
    
    ## create a generic funciton that takes a method to sort the episodes 
    