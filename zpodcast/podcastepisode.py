from datetime import datetime,date
from typing import Optional, Union
from dataclasses import dataclass
from pydantic import BaseModel

#from email.utils import parsedate_to_datetime
#import validators
#import json



class PodcastEpisode(BaseModel):
    title: str
    audio_url: Optional[str] = None
    pub_date: datetime = None
    description: str = None
    duration: str = None
    image_url: str = None
    episode_number: int = None




    
    # """
    # initializes a podcast episode object with the following attributes:
    # Args:
    #     title (str): The title of the episode.
    #     description (str): The description of the episode.
    #     audio_url (str): The URL of the audio file.
    #     duration (Optional[Union[int,str]], optional): The duration of the episode in seconds. Defaults to None.
    #     pub_date (Optional[date], optional): The publication date of the episode. Defaults to None.
    #     episode_number (Optional[int], optional): The episode number. Defaults to None.
    #     image_url (Optional[str], optional): The URL of the image for the episode. Defaults to None.
    # """

    # def __init__(self, title: str, 
    #             audio_url: str, 
    #             description: Optional[str] = "",
    #             pub_date: Optional[Union[datetime,str]] = None,
    #             duration: Optional[Union[int,str]] = None,
    #             episode_number: Optional[int] = None,
    #             image_url: Optional[str] = None):
    
    #     self.title = title
    #     self.description = description
    #     self.audio_url = audio_url
    #     self.duration = duration
    #     self.pub_date = pub_date
    #     self.episode_number = episode_number
    #     self.image_url = image_url


    # @property
    # def audio_url(self) -> Optional[str]:
    #     return self._audio_url

    # @audio_url.setter
    # def audio_url(self, value: Optional[str]) -> None:
    #     if value is not None:
    #         if validators.url(value):
    #             self._audio_url = value
    #         else:
    #             raise ValueError("Invalid audio URL")
    #     else:
    #         raise ValueError("Invalid audio URL")

    # """
    # Get the description of the episode.

    # Returns:
    #     str: The description of the episode.
    # """
    # @property
    # def description(self) -> str:
    #     return self._description
    
    # """
    # Set the description of the episode.

    # Args:
    #     value (str): The description of the episode.
    # """
    # @description.setter
    # def description(self, value: str) -> None:

    #     if not isinstance(value, str):
    #         self._description = ""
    #     else:
    #         self._description = value
        
    # """
    # Get the publication date of the episode.

    # Returns:
    #     Optional[date]: The publication date of the episode.
    # """
    # @property
    # def pub_date(self) -> datetime:
    #     return self._pub_date
    
    # """
    # Set the publication date of the episode.
    # Defaults to today's date if a pubdate is not set or not set correctly - swallows all errors

    # Args:
    #     value (Optional datetime or str): The publication date of the episode.
    # """
    # @pub_date.setter
    # def pub_date(self, value: Union[datetime, str]) -> None:
    #     # Validate that the value is a date object or string
    #     if value is not None:
    #         if isinstance(value, datetime):
    #             # if the value is a date object, set the publication date to the value
    #             self._pub_date = value 
    #         elif isinstance(value, date):
    #             # if the value is a date object, set the publication date to the value
    #             self._pub_date = value 
    #         elif isinstance(value, str):
    #             try:
    #                 # try parsing the string using the email.utils module
    #                 self._pub_date = parsedate_to_datetime(value)
    #             except:
    #                 self._pub_date = date.today()
    #         else:
    #             self._pub_date = date.today()
    #     else: # if the value is None, set the publication date to today's date
    #         self._pub_date = date.today()
        


    
    # """
    # Get the duration of the episode in seconds.

    # Returns:
    #     Optional[str]: The duration of the episode in seconds.
    # """
    # @property
    # def duration(self) -> Optional[int]:

    #     return self._duration
    
    # """
    # Set the duration of the episode in seconds from a string

    # Args:
    #     value (Optional[str]): The duration of the episode in seconds.
    # """
    # @duration.setter
    # def duration(self, value: Optional[str]) -> None:
    
    #     if value is not None:
    #         if isinstance(value, int):
    #             if value >= 0:
    #                 self._duration = value
    #             else:
    #                 self._duration = None
    #         else: 
    #             self._duration = None
    #     else:
    #         self._duration = None
            
            
    
    # @property
    # def episode_number(self) -> Optional[int]:
    #     return self._episode_number

    # @episode_number.setter
    # def episode_number(self, value: Optional[int]) -> None:
    #     if value is None:
    #         self._episode_number = None
    #     else:
    #         if isinstance(value, int):
    #             if value >= 0:
    #                 self._episode_number = value
    #             else:
    #                 self._episode_number = None
    #         else:
    #             self._episode_number = None
        
       


    # """
    # setter and getter for the image_url for the podcast episode.
    # Raises:
    #     ValueError: _description_

    # Returns:
    #     _type_: _description_
    # """
    # @property
    # def image_url(self) -> Optional[str]:
    #     return self._image_url

    # @image_url.setter
    # def image_url(self, value: Optional[str]) -> None:
    #     if value is not None:
    #         if validators.url(value):
    #             self._image_url = value
    #         else:
    #             self._image_url = None
    #     else:
    #         self._image_url = None

    # def toJson(self) -> str:
    #     """
    #     Returns the podcast episode as a JSON string.
    #     """
    #     return json.dumps(self, default=PodcastEpisode)