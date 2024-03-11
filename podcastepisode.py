from datetime import datetime, date
from typing import Optional, Union
from dataclasses import dataclass
from email.utils import parsedate_tz, mktime_tz
from zpodcast.podcastutils import is_valid_url
from urllib.parse import urlparse

"""
Represents a podcast episode and contains the following attributes.

Attributes:
    title (str): The title of the episode.
    description (str): The description of the episode.
    audio_url (str): The URL of the audio file.
    duration (Optional[str], optional): a string repreesentation of the duration of the episode in minutes. Defaults to None.
    duration_in_seconds (Optional[int], optional): The duration of the episode in seconds. Defaults to None.
    pub_date (Optional[date], optional): The publication date of the episode. Defaults to None.
    episode_number (Optional[int], optional): The episode number. Defaults to None.
    podcast_url (str): The URL of the podcast. Defaults to None.
"""
@dataclass
class PodcastEpisode:
    title: str
    description: str
    _audio_url: str
    _duration: Optional[str] = None
    _podcast_episode_image_url: Optional[str] = None
    _pub_date: Optional[date] = None
    _episode_number: Optional[int] = None
    podcast_url: Optional[str] = None
    #podcast : Optional[PodcastData] = None
    
    @dataclass
    class PodcastEpisode:
        # ...

        @property
        def podcast_episode_image_url(self) -> Optional[str]:
            return self._podcast_episode_image_url


        @podcast_episode_image_url.setter
        def podcast_episode_image_url(self, value: Optional[str]) -> None:
            if value is None or is_valid_url(value):
                self._podcast_episode_image_url = value
            else:
                raise ValueError("Invalid URL")


    
    """
    __init__ method
    Initializes a PodcastEpisode object with the given attributes.

    Args:
        title (str): The title of the episode.
        description (str): The description of the episode.
        audio_url (str): The URL of the audio file.
        duration (Optional[str], optional): The duration of the episode in seconds. Defaults to None.
        pub_date (Optional[date], optional): The publication date of the episode. Defaults to None.
        episode_number (Optional[int], optional): The episode number. Defaults to None.
    """
    def __init__(self, title: str, description: str, audio_url: str, duration: Optional[Union[int,str]] = None,
             pub_date: Optional[date] = None,
            episode_number: Optional[int] = None):
       

        self.title = title
        self.description = description
        self.audio_url = audio_url
        self.duration = duration
        self.pub_date = pub_date
        self.episode_number = episode_number

    
    """
    Get the duration of the episode in seconds.

    Returns:
        Optional[str]: The duration of the episode in seconds.
    """
    @property
    def duration(self) -> Optional[int]:

        return self._duration
    
    """
    Set the duration of the episode in seconds from a string

    Args:
        value (Optional[str]): The duration of the episode in seconds.
    """
    @duration.setter
    def duration(self, value: Optional[str]) -> None:
    
        if value is not None:
            try:
                self._duration = int(value)
            except ValueError:
                raise ValueError("Invalid duration")
            
    """
    Get the publication date of the episode.

    Returns:
        Optional[date]: The publication date of the episode.
    """
    @property
    def pub_date(self) -> Optional[date]:

        return self._pub_date
    
    """
    Set the publication date of the episode.

    Args:
        value (Optional[date]): The publication date of the episode.
    """
    @pub_date.setter
    def pub_date(self, value: Optional[date]) -> None:
    
        if isinstance(value, str):
            timestamp = parsedate_tz(value)
            if timestamp is not None:
                self._pub_date = datetime.fromtimestamp(mktime_tz(timestamp))
            else:
                self._pub_date = None
        elif isinstance(value, date):
            self._pub_date = value
        else:
            self._pub_date = None
            
    @property
    def audio_url(self) -> Optional[str]:
        return self._audio_url

    @audio_url.setter
    def audio_url(self, value: Optional[str]) -> None:
        if value is not None:
            parsed_url = urlparse(value)
            if parsed_url.scheme and parsed_url.netloc:
                self._audio_url = value
            else:
                raise ValueError("Invalid audio URL")
        else:
            raise ValueError("Invalid audio URL")
        
        
    @property
    def episode_number(self) -> Optional[int]:
        return self._episode_number

    @episode_number.setter
    def episode_number(self, value: Optional[int]) -> None:
        if value is not None and not isinstance(value, int):
            raise ValueError("Episode number must be an integer")
        self._episode_number = value



