from dataclasses import asdict, dataclass, field
import validators
from typing import Optional, List, Dict
from zpodcast.core.playlist import PodcastEpisodeList
from zpodcast.parsers.rss import RSSPodcastParser

@dataclass
class PodcastData:
    """
    Represents the data of a podcast.
    """

    _title: str
    _podcast_url: str
    _host: Optional[str]
    _description: Optional[str]
    _podcast_priority: Optional[int]
    _image_url: Optional[str]
    _episodelists : Optional[List[PodcastEpisodeList]]
    _name_set_manually: bool

    def __init__(self, title:str, 
                 podcast_url: str, 
                 host:str = None, 
                 description:str = None, 
                 episodelists:List[PodcastEpisodeList]=[], 
                 podcast_priority:int=None, 
                 image_url:str=None,
                 name_set_manually:bool=False):
        """
        Initializes a new instance of the PodcastData class.

        Args:
            title (str): The title of the podcast.
            host (str): The host of the podcast.
            description (str): The description of the podcast.
            episodes (PodcastList): The episodes of the podcast.
            podcast_priority (int): The priority of the podcast.
            image_url (str): The image URL of the podcast.
            name_set_manually (bool): Indicates if the name was set manually.
        """

        self.title = title
        self.podcast_url = podcast_url
        self.host = host
        self.description = description
        self.episodelists = episodelists
        self.podcast_priority = podcast_priority
        self.image_url = image_url
        self.name_set_manually = name_set_manually
        self.populate_episodes_from_feed()
        


    """
    getter setter for Title variable

    """
    @property
    def title(self):
        """
        Gets the title of the podcast.

        Returns:
            str: The title of the podcast.
        """
        return self._title
    
    @title.setter
    def title(self, value):
        """
        Sets the title of the podcast.

        Args:
            value (str): The title to set for the podcast.
        """
        if value is None or not isinstance(value, str):
            raise ValueError("Invalid title")
        
        self._title = value

    """
    podcast url getter setters
    """
    @property
    def podcast_url(self):
        """
        Gets the podcast URL.

        Returns:
            str: The podcast URL.
        """
        return self._podcast_url

    @podcast_url.setter
    def podcast_url(self, value):
        """
        Sets the podcast URL.

        Args:
            value (str): The podcast URL to set.

        Raises:
            ValueError: If the podcast URL is invalid.
        """
        if value is not None:
            if not validators.url(value):
                raise ValueError("Invalid podcast URL")
        else:
            raise ValueError("Invalid podcast URL")
        
        self._podcast_url = value

    @property
    def episodelists(self):

        return self._episodelists
    
    @episodelists.setter
    def episodelists(self, value):

        self._episodelists = []
        if isinstance(value, List):
            for item in value:
                if not isinstance(item, PodcastEpisodeList):
                    pass
                else:
                    self._episodelists.append(item)

    """
    Getter setter for host
    """
    @property
    def host(self):
        """
        Gets the host of the podcast.

        Returns:
            str: The host of the podcast.
        """
        return self._host   
    
    @host.setter
    def host(self, value:str):
        """
        Sets the host of the podcast.

        Args:
            value (str): The host to set for the podcast.
        """
        if value is not None:
            if isinstance(value, str):
                self._host = value
            
            if not isinstance(value, str):
                self._host = ""
        
        if value is None:
            self._host = ""

    """
    getter setter for description
    """
    @property
    def description(self):
        """
        Gets the description of the podcast.

        Returns:
            str: The description of the podcast.
        """
        return self._description
    
    @description.setter
    def description(self, value):
        """
        Sets the description of the podcast.

        Args:
            value (str): The description to set for the podcast.
        """
        if value is not None:
            if not isinstance(value, str):
                value = ""
        else:
            value = ""
                
        self._description = value    
    
    """
    getter setter for priority with a clamping of the priority between -10 and 10
    """
    @property
    def podcast_priority(self) -> int:
        """
        Gets the priority value.

        Returns:
            int: The priority value.
        """
        return self._podcast_priority
    
    @podcast_priority.setter
    def podcast_priority(self, value: int):
        """
        Sets the priority value.

        Args:
            value (int): The priority value to set.

        Raises:
            ValueError: If the priority value is not an integer or is out of range.
        """
        self._podcast_priority = self._clamp_priority(value)
        

    def _clamp_priority(self, value:int) -> int:
        """
        Clamps the priority value between -10 and 10.
        """

        if value is not None:
            if isinstance(value, int):  
                value = max(-10, min(10, value))
            else:
                value = 0
        return value
    
    @property
    def image_url(self):
        """
        Gets the image URL.

        Returns:
            str: The image URL.
        """
        return self._image_url
    
    @image_url.setter
    def image_url(self, value):
        """
        Sets the image URL.

        Args:
            value (str): The image URL to set.

        Raises:
            ValueError: If the image URL is invalid.
        """
        self._image_url = value

    @property
    def name_set_manually(self):
        """
        Gets the value indicating if the name was set manually.

        Returns:
            bool: The value indicating if the name was set manually.
        """
        return self._name_set_manually

    @name_set_manually.setter
    def name_set_manually(self, value):
        """
        Sets the value indicating if the name was set manually.

        Args:
            value (bool): The value to set.
        """
        if not isinstance(value, bool):
            raise ValueError("Invalid value for name_set_manually")
        self._name_set_manually = value
 
    def populate_episodes_from_feed(self) -> None:
        # retrieve the list of episodes from the podcast URL
        episodes = RSSPodcastParser.get_episodes(self.podcast_url)
        
        # prepare updating the episode name to match the podcast's title with the suffix "episode list"
        episode_list_name = f"{self.title} episode list"
        
        # create a podcast episode list that can then be used to determine which of the episodes are new.
        new_episode_list = PodcastEpisodeList(name=episode_list_name, episodes=episodes)
        
        # determine which episodes are new and append the new episodes to the existing list of episodes for this podcast.
        self.episodelists = [new_episode_list]
        
        self.name_set_manually = False
        
        # Update podcast metadata
        feed = RSSPodcastParser.get_rss_metadata(self.podcast_url)
        self.host = feed.get('author')
        self.description = feed.get('description')
        #self.image_url = feed.get('image')

 
    def to_dict(self) -> Dict:
        podcastdata_dict = {"title": self.title, 
                            "podcast_url": self.podcast_url,
                            "host": self.host,
                            "podcast_priority": self.podcast_priority,
                            "image_url": self.image_url,
                            "description": self.description,
                            "episodelists" : [playlist.to_dict() for playlist in self.episodelists],
                            "name_set_manually": self.name_set_manually
        }
        return(podcastdata_dict)                                   

    @classmethod
    def from_dict(cls, data: Dict):
        episodelists = data.get("episodelists", [])
        podcastdata = PodcastData(title=data.get("title"),
                                  podcast_url=data.get("podcast_url"),
                                  host = data.get("host"),
                                  description=data.get("description"),
                                  podcast_priority = data.get("podcast_priority"),
                                  image_url = data.get("image_url"),
                                  episodelists = [PodcastEpisodeList.from_dict(playlist_data) for playlist_data in episodelists],
                                  name_set_manually = data.get("name_set_manually", False)            
        )
        return podcastdata
