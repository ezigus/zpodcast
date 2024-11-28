from dataclasses import asdict, dataclass
import validators
from typing import Optional, List
from zpodcast.podcastepisodelist import PodcastEpisodeList

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
    _episodes : Optional[PodcastEpisodeList]

    def __init__(self, title:str, 
                 podcast_url: str, 
                 host:str = None, 
                 description:str = None, 
                 episodes:PodcastEpisodeList=None, 
                 podcast_priority:int=None, 
                 image_url:str=None):
        """
        Initializes a new instance of the PodcastData class.

        Args:
            title (str): The title of the podcast.
            host (str): The host of the podcast.
            description (str): The description of the podcast.
            episodes (PodcastList): The episodes of the podcast.
            podcast_priority (int): The priority of the podcast.
            image_url (str): The image URL of the podcast.
        """

        self.title = title
        self.podcast_url = podcast_url
        self.host = host
        self.description = description
        self.episodes = episodes
        self.podcast_priority = podcast_priority
        self.image_url = image_url
        dict()

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
    def episodes(self):
        return self._episodes
    
    @episodes.setter
    def episodes(self, value):
        if not isinstance(value, PodcastEpisodeList):
            self._episodes = []
        else:
            self._episodes = value

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



    # """
    # getter setter for image_url with a validation method for the URL
    # """
    # def validate_image_url(self):
    #     """
    #     Validates the image URL.

    #     Returns:
    #         bool: True if the image URL is valid, False otherwise.
    #     """
    #     if self._image_url is not None:
    #         return is_valid_url(self._image_url)
    #     return False
    
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
 
 

    def to_dict(self):
        podcastdata_dict = {
            "title" : self.title,
            "podcast_url" : self.podcast_url,
            "host" : self.host,
            "description" : self.description,
            "episode_list" : self.episodes.to_dict(),
            "podcast_priority" : self.podcast_priority,
            "image_url" : self.image_url
        }
        return podcastdata_dict

    @classmethod
    def from_dict(cls, data):
        
        podcastdata = PodcastData(data["title"], 
                                  data["podcast_url"],
                                  data["host"], 
                                  data["description"],
                                  PodcastEpisodeList(data["episode_list"]),
                                  data["podcast_priority"],
                                  data["image_url"]
        )
        
        return cls(**data)
