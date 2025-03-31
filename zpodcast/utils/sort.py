from dataclasses import dataclass
from typing import List, Optional


@dataclass
class SortParameters:
    _episode_title: Optional[str]
    _episode_duration: Optional[int]
    _episode_date: Optional[str]
    _episode_rating: Optional[float]
    _podcast_title: Optional[str]
    _podcast_author: Optional[str]

    @property
    def episode_title(self) -> Optional[str]:
        return self._episode_title

    @episode_title.setter
    def episode_title(self, value: Optional[str]) -> None:
        if value is None or value == "A-Z" or value == "Z-A":
            self._episode_title = value
        else:
            raise ValueError("Invalid sort option for title")

    @property
    def episode_duration(self) -> Optional[int]:
        return self._episode_duration

    @episode_duration.setter
    def episode_duration(self, value: Optional[str]) -> None:
        if value is None or value == "ShortToLong" or value == "LongToShort":
            self._episode_duration = value
        else:
            raise ValueError("Invalid sort option for duration")

    @property
    def episode_date(self) -> Optional[str]:
        return self._episode_date

    @episode_date.setter
    def episode_date(self, value: Optional[str]) -> None:
        if value is None or value == "Earliest" or value == "Latest":
            self._episode_date = value
        else:
            raise ValueError("Invalid sort option for date")

    @property
    def episode_rating(self) -> Optional[float]:
        return self._episode_rating

    @episode_rating.setter
    def episode_rating(self, value: Optional[float]) -> None:
        if value is None or value == "highest" or value == "lowest":
            self._episode_rating = value
        else:
            raise ValueError("Invalid sort option for rating")

    @property
    def episode_tags(self) -> Optional[List[str]]:
        return self._episode_tags

    @episode_tags.setter
    def episode_tags(self, value: Optional[List[str]]) -> None:
        self._episode_tags = value

    @property
    def podcast_title(self) -> Optional[str]:
        return self._podcast_title

    @podcast_title.setter
    def podcast_title(self, value: Optional[str]) -> None:
        if value is None or value == "A-Z" or value == "Z-A":
            self._podcast_title = value
        else:
            raise ValueError("Invalid sort option for podcast title")

    @property
    def podcast_author(self) -> Optional[str]:
        return self._podcast_author

    @podcast_author.setter
    def podcast_author(self, value: Optional[str]) -> None:
        if value is None or value == "A-Z" or value == "Z-A":
            self._podcast_author = value
        else:
            raise ValueError("Invalid sort option for podcast author")

    @property
    def podcast_category(self) -> Optional[str]:
        return self._podcast_category

    @podcast_category.setter
    def podcast_category(self, value: Optional[str]) -> None:
        self._podcast_category = value




