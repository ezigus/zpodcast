import pytest
import dataclasses
from email.utils import parsedate_to_datetime
from datetime import date, datetime
from zpodcast.core.episode import PodcastEpisode
from unittest.mock import patch


# Validate that PodcastEpisode is a dataclass
def test_podcastepisode_is_dataclass():
    assert dataclasses.is_dataclass(PodcastEpisode)


# Test the title attribute
def test_podcastepisode_title():
    # Create a podcast episode object
    episode = PodcastEpisode(title="Episode 1",
                             description="Episode 1 description",
                             audio_url="https://example.com/episode1.mp3",
                             pub_date=" Mon, 11 Apr 2016 15:00:00 +0100")

    # Test the title attribute of the podcast episode
    assert episode.title == "Episode 1"


def test_podcastepisode_no_title():
    with pytest.raises(TypeError):
        # Variable is intentionally not used, as we're testing the exception
        PodcastEpisode(description="Episode 1 description",
                       audio_url="https://example.com/episode1.mp3",
                       pub_date=" Mon, 11 Apr 2016 15:00:00 +0100")


# Test the description attribute
def test_podcastepisode_description():
    episode = PodcastEpisode(title="Episode 1", audio_url="https://example.com/episode1.mp3", description="Episode 1 description")
    assert episode.description == "Episode 1 description"


def test_podcastepisode_no_description():
    episode = PodcastEpisode(title="Episode 1",
                             audio_url="https://example.com/episode1.mp3",
                             pub_date=" Mon, 11 Apr 2016 15:00:00 +0100")
    assert episode.description == ""


def test_podcastepisode_description_invalid():
    # Create a podcast episode object with an empty description
    episode = PodcastEpisode(title="Episode 1",
                             description=datetime.now(),
                             audio_url="https://example.com/episode1.mp3",
                             pub_date=" Mon, 11 Apr 2016 15:00:00 +0100")

    # Test the description attribute of the podcast episode
    assert episode.description == ""


"""
Tests to verify the duration values in this data class
"""


def test_podcastepisode_duration_string():
    # Create a podcast episode object
    episode = PodcastEpisode(title="Episode 1",
                             description="Episode 1 description",
                             audio_url="https://example.com/episode1.mp3",
                             duration="1800",
                             pub_date=" Mon, 11 Apr 2016 15:00:00 +0100")
    
    # Test the duration attribute of the podcast episode
    assert episode.duration == 1800  # String duration should be converted to integer


def test_podcastepisode_duration_int():
    # Create a podcast episode object
    episode = PodcastEpisode(title="Episode 1",
                             description="Episode 1 description",
                             audio_url="https://example.com/episode1.mp3",
                             duration=1800,
                             pub_date=" Mon, 11 Apr 2016 15:00:00 +0100")

    assert episode.duration == 1800


def test_podcastepisode_duration_none():
    # Create a podcast episode object
    episode = PodcastEpisode(title="Episode 1",
                             description="Episode 1 description",
                             audio_url="https://example.com/episode1.mp3",
                             pub_date=" Mon, 11 Apr 2016 15:00:00 +0100")

    assert episode.duration is None


def test_podcastepisode_duration_nonint():
    # Create a podcast episode object with invalid duration (non int)
    episode = PodcastEpisode(title="Episode 1",
                             description="Episode 1 description",
                             audio_url="https://example.com/episode1.mp3",
                             duration="1800seconds",
                             pub_date=" Mon, 11 Apr 2016 15:00:00 +0100")
    assert episode.duration is None


def test_podcastepisode_duration_negative():
    # Create a podcast episode object with invalid duration (negative int)
    episode = PodcastEpisode(title="Episode 1",
                             description="Episode 1 description",
                             audio_url="https://example.com/episode1.mp3",
                             duration=-1800,
                             pub_date=" Mon, 11 Apr 2016 15:00:00 +0100")
    assert episode.duration is None


def test_podcastepisode_duration_zero():
    # Create a podcast episode object with invalid duration (negative int)
    episode = PodcastEpisode(title="Episode 1",
                             description="Episode 1 description",
                             audio_url="https://example.com/episode1.mp3",
                             duration=0,
                             pub_date=" Mon, 11 Apr 2016 15:00:00 +0100")
    assert episode.duration == 0


def test_podcastepisode_duration_emptyquote():
    # Create a podcast episode object with invalid duration (negative int)
    episode = PodcastEpisode(title="Episode 1",
                             description="Episode 1 description",
                             audio_url="https://example.com/episode1.mp3",
                             duration="",
                             pub_date=" Mon, 11 Apr 2016 15:00:00 +0100")
    assert episode.duration is None


"""
Tests to verify the pub_date values in this data class
"""


def test_podcastepisode_pub_date():
    # Create a podcast episode object
    episode = PodcastEpisode(title="Episode 1",
                             description="Episode 1 description",
                             audio_url="https://example.com/episode1.mp3",
                             duration=1800,
                             pub_date="Mon, 11 Apr 2016 15:15:15 +1500")

    # Test the publication date attribute of the podcast episode
    assert episode.pub_date == parsedate_to_datetime("Mon, 11 Apr 2016 15:15:15 +1500")


def test_podcastepisode_pub_date_datetime():
    # Create a podcast episode object with a datetime object
    dt = datetime(2016, 4, 11, 15, 15, 15)
    
    episode = PodcastEpisode(title="Episode 1",
                             description="Episode 1 description",
                             audio_url="https://example.com/episode1.mp3",
                             duration=1800,
                             pub_date=dt)

    # Test the publication date attribute of the podcast episode
    assert episode.pub_date == dt


def test_podcastepisode_pub_date_date():
    # Create a podcast episode object with a date object
    episode = PodcastEpisode(title="Episode 1",
                             description="Episode 1 description",
                             audio_url="https://example.com/episode1.mp3",
                             duration=1800,
                             pub_date=date.today())

    # Test the publication date attribute of the podcast episode
    assert episode.pub_date == date.today()


def test_podcastepisode_pub_date_none():
    # Create a podcast episode object
    episode = PodcastEpisode(title="Episode 1",
                             description="Episode 1 description",
                             audio_url="https://example.com/episode1.mp3")
    assert episode.pub_date == date.today()


def test_podcastepisode_pub_date_invalid_number():
    episode = PodcastEpisode(title="Episode 1",
                             description="Episode 1 description",
                             audio_url="https://example.com/episode1.mp3",
                             duration=1800,
                             pub_date=1234)
    assert episode.pub_date == date.today()


def test_podcastepisode_pub_date_invalid_str():
    episode = PodcastEpisode(title="Episode 1",
                             description="Episode 1 description",
                             audio_url="https://example.com/episode1.mp3",
                             duration=1800,
                             pub_date="1234")
    assert episode.pub_date == date.today()


def test_podcastepisode_pub_date_incompletedatetime():
    episode = PodcastEpisode(title="Episode 1",
                             description="Episode 1 description",
                             audio_url="https://example.com/episode1.mp3",
                             duration=1800,
                             pub_date="12/01/2001")
    assert episode.pub_date == date.today()


"""
Tests to verify the image url is actually valid and set correctly
"""


@patch("zpodcast.core.episode.validators.url", return_value=True)
def test_podcastepisode_audio_url(mock_validators):
    episode = PodcastEpisode(title="Episode 1", audio_url="https://example.com/episode1.mp3")
    assert episode.audio_url == "https://example.com/episode1.mp3"
    mock_validators.assert_called_once_with("https://example.com/episode1.mp3")


@patch("zpodcast.core.episode.validators.url", return_value=False)
def test_podcastepisode_audio_url_invalid(mock_validators):
    with pytest.raises(ValueError, match="^Invalid audio URL$"):
        PodcastEpisode(title="Episode 1", audio_url="invalid_url")
    mock_validators.assert_called_once_with("invalid_url")


def test_podcastepisode_audio_url_badscheme():
    # Create a podcast episode object with an invalid scheme
    with pytest.raises(ValueError, match="^Invalid audio URL$"):
        # Variable intentionally not used as we're testing the exception
        PodcastEpisode(title="Episode 1",
                       description="Episode 1 description",
                       audio_url="ft//example.com/episode1.mp3",
                       pub_date=" Mon, 11 Apr 2016 15:00:00 +0100")


def test_podcastepisode_audio_url_badnetloc():
    # Create a podcast episode object with an invalid scheme
    with pytest.raises(ValueError, match="^Invalid audio URL$"):
        # Variable intentionally not used as we're testing the exception
        PodcastEpisode(title="Episode 1",
                       description="Episode 1 description",
                       audio_url="ftp:///episode1.mp3",
                       pub_date=" Mon, 11 Apr 2016 15:00:00 +0100")


def test_podcastepisode_invalid_audio_url():
    # Create a podcast episode object with an invalid audio URL
    with pytest.raises(ValueError, match="^Invalid audio URL$"):
        # Variable intentionally not used as we're testing the exception
        PodcastEpisode(title="Episode 1",
                       description="Episode 1 description",
                       audio_url="invalid_url",
                       pub_date=" Mon, 11 Apr 2016 15:00:00 +0100")


def test_podcastepisode_no_audio_url():
    # Create a podcast episode object with no audio URL
    with pytest.raises(TypeError):
        # Variable intentionally not used as we're testing the exception
        PodcastEpisode(title="Episode 1",
                       description="Episode 1 description",
                       pub_date=" Mon, 11 Apr 2016 15:00:00 +0100")


def test_podcastepisode_audio_url_none():
    # Create a podcast episode object with no audio URL
    with pytest.raises(ValueError, match="^Invalid audio URL$"):
        # Variable intentionally not used as we're testing the exception
        PodcastEpisode(title="Episode 1",
                       description="Episode 1 description",
                       audio_url=None,
                       pub_date=" Mon, 11 Apr 2016 15:00:00 +0100")


"""
Tests to verify the episode_number values in this data class
"""


def test_podcastepisode_episode_number_none():
    # Create a podcast episode object with no episode number
    episode = PodcastEpisode(title="Episode 1",
                             description="Episode 1 description",
                             audio_url="https://example.com/episode1.mp3",
                             pub_date=" Mon, 11 Apr 2016 15:00:00 +0100")

    # Test the episode_number attribute of the podcast episode
    assert episode.episode_number is None


def test_podcastepisode_episode_number():
    # Create a podcast episode object with an episode number
    episode = PodcastEpisode(title="Episode 1",
                             description="Episode 1 description",
                             audio_url="https://example.com/episode1.mp3",
                             episode_number=10,
                             pub_date=" Mon, 11 Apr 2016 15:00:00 +0100")

    # Test the episode_number attribute of the podcast episode
    assert episode.episode_number == 10


def test_podcastepisode_episode_number_negative():
    # Create a podcast episode object with a negative episode number
    episode = PodcastEpisode(title="Episode 1",
                             description="Episode 1 description",
                             audio_url="https://example.com/episode1.mp3",
                             episode_number=-1,
                             pub_date=" Mon, 11 Apr 2016 15:00:00 +0100")
    assert episode.episode_number is None


def test_podcastepisode_episode_number_zero():
    # Create a podcast episode object with a zero episode number
    episode = PodcastEpisode(title="Episode 1",
                             description="Episode 1 description",
                             audio_url="https://example.com/episode1.mp3",
                             episode_number=0,
                             pub_date=" Mon, 11 Apr 2016 15:00:00 +0100")
    assert episode.episode_number == 0


def test_podcastepisode_episode_number_nonint():
    # Create a podcast episode object with a non-integer episode number
    episode = PodcastEpisode(title="Episode 1",
                             description="Episode 1 description",
                             audio_url="https://example.com/episode1.mp3",
                             episode_number=datetime.now(),
                             pub_date=" Mon, 11 Apr 2016 15:00:00 +0100")
    assert episode.episode_number is None


def test_podcastepisode_episode_number_invalid():
    # Create a podcast episode object with an invalid episode number
    episode = PodcastEpisode(title="Episode 1",
                             description="Episode 1 description",
                             audio_url="https://example.com/episode1.mp3",
                             episode_number="one",
                             pub_date=" Mon, 11 Apr 2016 15:00:00 +0100")
    assert episode.episode_number is None


def test_podcastepisode_episode_number_emptyquote():
    # Create a podcast episode object with a negative episode number
    episode = PodcastEpisode(title="Episode 1",
                             description="Episode 1 description",
                             audio_url="https://example.com/episode1.mp3",
                             episode_number="",
                             pub_date=" Mon, 11 Apr 2016 15:00:00 +0100")
    assert episode.episode_number is None


"""
Test the podcastepisode image url is actually valid and set correctly
"""


@patch("zpodcast.core.episode.validators.url")
def test_podcastepisode_image_url_with_validator(mock_validators):
    # Configure the mock to return True only for the image URL
    mock_validators.side_effect = lambda url: True
    
    episode = PodcastEpisode(title="Episode 1", audio_url="https://example.com/episode1.mp3", image_url="https://example.com/episode1.jpg")
    assert episode.image_url == "https://example.com/episode1.jpg"


@patch("zpodcast.core.episode.validators.url")
def test_podcastepisode_image_url_with_invalid_validator(mock_validators):
    # Configure the mock to return True for audio URLs but False for image URLs
    mock_validators.side_effect = lambda url: url == "https://example.com/episode1.mp3"
    
    episode = PodcastEpisode(title="Episode 1", audio_url="https://example.com/episode1.mp3", image_url="invalid_url")
    assert episode.image_url is None


def test_podcastepisode_image_url_none():
    # Create a podcast episode object with no image URL
    episode = PodcastEpisode(title="Episode 1", description="Episode 1 description", audio_url="https://example.com/episode1.mp3", pub_date=" Mon, 11 Apr 2016 15:00:00 +0100")

    # Test the podcast_episode_image_url attribute of the podcast episode
    assert episode.image_url is None


def test_podcastepisode_image_url():
    # Create a podcast episode object with an image URL
    episode = PodcastEpisode(title="Episode 1",
                             description="Episode 1 description",
                             audio_url="https://example.com/episode1.mp3",
                             pub_date=" Mon, 11 Apr 2016 15:00:00 +0100",
                             image_url="https://example.com/episode1.jpg")
    
    # Test the podcast_episode_image_url attribute of the podcast episode
    assert episode.image_url == "https://example.com/episode1.jpg"


def test_podcastepisode_image_url_invalid_nonvalidator():
    # Create a podcast episode object with an invalid image URL
    episode = PodcastEpisode(title="Episode 1",
                             description="Episode 1 description",
                             audio_url="https://example.com/episode1.mp3",
                             pub_date=" Mon, 11 Apr 2016 15:00:00 +0100",
                             image_url="invalid_url")
    assert episode.image_url is None


def test_podcastepisode_image_url_emptyquotes():
    # Create a podcast episode object with no image URL
    episode = PodcastEpisode(title="Episode 1",
                             description="Episode 1 description",
                             audio_url="https://example.com/episode1.mp3",
                             pub_date=" Mon, 11 Apr 2016 15:00:00 +0100",
                             image_url="")
    assert episode.image_url is None


def test_podcastepisode_to_dict():
    episode = PodcastEpisode(
        title="Episode 1",
        audio_url="https://example.com/episode1.mp3",
        description="Episode 1 description",
        pub_date="Mon, 11 Apr 2016 15:00:00 +0100",
        duration=1800,
        episode_number=1,
        image_url="https://example.com/episode1.jpg"
    )
    episode_dict = episode.to_dict()
    assert episode_dict == {
        "title": "Episode 1",
        "audio_url": "https://example.com/episode1.mp3",
        "description": "Episode 1 description",
        "pub_date": "2016-04-11T15:00:00+01:00",
        "duration": 1800,
        "episode_number": 1,
        "image_url": "https://example.com/episode1.jpg"
    }


def test_podcastepisode_from_dict():
    episode_dict = {
        "title": "Episode 1",
        "audio_url": "https://example.com/episode1.mp3",
        "description": "Episode 1 description",
        "pub_date": "2016-04-11T14:00:00+00:00",
        "duration": 1800,
        "episode_number": 1,
        "image_url": "https://example.com/episode1.jpg"
    }
    episode = PodcastEpisode.from_dict(episode_dict)
    assert episode.title == "Episode 1"
    assert episode.audio_url == "https://example.com/episode1.mp3"
    assert episode.description == "Episode 1 description"
    assert episode.pub_date == datetime.fromisoformat("2016-04-11T14:00:00+00:00")
    assert episode.duration == 1800
    assert episode.episode_number == 1
    assert episode.image_url == "https://example.com/episode1.jpg"
