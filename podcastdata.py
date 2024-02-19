from dataclasses import dataclass
from typing import Optional
from podcastepisode import PodcastEpisode
from podcastutils import is_valid_url
from typing import List


@dataclass
class PodcastData:
    """
    Represents the data of a podcast.

    Attributes:
        title (str): The title of the podcast.
        host (str): The host of the podcast.
        description (str): The description of the podcast.
        episodes (PodcastEpisode): The episodes of the podcast.
        priority (Optional[int]): The priority of the podcast (optional).
        _image_url (Optional[str]): The URL of the podcast's image (optional).

    Methods:
        __post_init__(): Initializes the PodcastData object and validates the priority.
        validate_image_url(): Validates the image URL.
        image_url(): Gets the image URL.
        image_url(value): Sets the image URL.
        clamp_priority(): Clamps the priority value between -10 and 10.
    """

    title: str
    host: str
    description: str
    episodes: List[PodcastEpisode]
    priority: Optional[int] = None
    _image_url: Optional[str] = None

    def clamp_priority(self):
        """
        Clamps the priority value between -10 and 10.
        """
        if self.priority is not None:
            self.priority = max(-10, min(10, self.priority))

    def __post_init__(self):
        """
        Initializes the PodcastData object and validates the priority.

        The priority is clamped between -10 and 10.
        """
        if self.priority is not None:
            self.priority = max(-10, min(10, self.priority))

    def validate_image_url(self):
        """
        Validates the image URL.

        Returns:
            bool: True if the image URL is valid, False otherwise.
        """
        if self._image_url is not None:
            return is_valid_url(self._image_url)
        return False
    
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
        if is_valid_url(value):
            self._image_url = value
        else:
            raise ValueError("Invalid image URL")

