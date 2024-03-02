import pytest
from email.utils import parsedate_tz
from zpodcast.podcastepisode import PodcastEpisode

"""
tests to validate the setting of retrieval of the title
"""
# validate the title is set correctly
def test_podcastepisode_title():
    # Create a podcast episode object
    episode = PodcastEpisode(title="Episode 1", description="Episode 1 description", audio_url="https://example.com/episode1.mp3")

    # Test the title attribute of the podcast episode
    assert episode.title == "Episode 1"

"""
tests to validate the setting of retrieval of the description
"""
def test_podcastepisode_description():
    # Create a podcast episode object
    episode = PodcastEpisode(title="Episode 1", description="Episode 1 description", audio_url="https://example.com/episode1.mp3")

    # Test the description attribute of the podcast episode
    assert episode.description == "Episode 1 description"

# negative testing, not submitting a description
def test_podcastepisode_no_description():
    with pytest.raises(TypeError):
        episode = PodcastEpisode(title="Episode 1", audio_url="https://example.com/episode1.mp3")


"""
Tests to verify the duration values in this data class
"""
def test_podcastepisode_duration_string():
    # Create a podcast episode object
    episode = PodcastEpisode(title="Episode 1", description="Episode 1 description", audio_url="https://example.com/episode1.mp3", duration="1800")

    # Test the duration attribute of the podcast episode
    assert episode.duration == 1800
    
def test_podcastepisode_duration_int():
    # Create a podcast episode object
    episode = PodcastEpisode(title="Episode 1", description="Episode 1 description", audio_url="https://example.com/episode1.mp3", duration=1800)

    assert episode.duration == 1800
    
def test_podcastepisode_duration_none():
    # Create a podcast episode object
    episode = PodcastEpisode(title="Episode 1", description="Episode 1 description", audio_url="https://example.com/episode1.mp3")

    assert episode.duration is None
    
def test_podcastepisode_duration_nonint():
    with pytest.raises(ValueError):
        episode = PodcastEpisode(title="Episode 1", description="Episode 1 description", audio_url="https://example.com/episode1.mp3", duration="1800s")
    

    


"""
Tests to verify the pub_date values in this data class
"""

def test_podcastepisode_pub_date_none():
    # Create a podcast episode object
    episode = PodcastEpisode(title="Episode 1", description="Episode 1 description", audio_url="https://example.com/episode1.mp3", duration=1800)

    # Test the publication date attribute of the podcast episode
    assert episode.pub_date == None
    
def test_podcastepisode_pub_date():
    # Create a podcast episode object
    episode = PodcastEpisode(title="Episode 1", description="Episode 1 description", audio_url="https://example.com/episode1.mp3", duration=1800, pub_date="2021-01-01")

    # Test the publication date attribute of the podcast episode
    assert episode.pub_date == parsedate_tz("2021-01-01")
    
def test_podcastepisode_pub_date_invalid_number():
    episode = PodcastEpisode(title="Episode 1", description="Episode 1 description", audio_url="https://example.com/episode1.mp3", duration=1800, pub_date=1234)

    # Test the publication date attribute of the podcast episode
    assert episode.pub_date == None

def test_podcastepisode_pub_date_invalid_str():
    episode = PodcastEpisode(title="Episode 1", description="Episode 1 description", audio_url="https://example.com/episode1.mp3", duration=1800, pub_date="1234")

    # Test the publication date attribute of the podcast episode
    assert episode.pub_date == None

"""
testing that the audio URL is properly set and formatted
"""

def test_podcastepisode_audio_url():
    # Create a podcast episode object with a valid audio URL
    episode = PodcastEpisode(title="Episode 1", description="Episode 1 description", audio_url="https://example.com/episode1.mp3")

    # Test the audio_url attribute of the podcast episode
    assert episode.audio_url == "https://example.com/episode1.mp3"

def test_podcastepisode_invalid_audio_url():
    # Create a podcast episode object with an invalid audio URL
    with pytest.raises(ValueError):
        episode = PodcastEpisode(title="Episode 1", description="Episode 1 description", audio_url="invalid_url")
        
def test_podcastepisode_no_audio_url():
    # Create a podcast episode object with no audio URL
    with pytest.raises(TypeError):
        episode = PodcastEpisode(title="Episode 1", description="Episode 1 description")

def test_podcastepisode_audo_url_none():
    # Create a podcast episode object with no audio URL
    with pytest.raises(ValueError):
        episode = PodcastEpisode(title="Episode 1", description="Episode 1 description", audio_url=None)
        
""" 
Tests to verify the episode_number values in this data class
"""
def test_podcastepisode_episode_number_none():
    # Create a podcast episode object with no episode number
    episode = PodcastEpisode(title="Episode 1", description="Episode 1 description", audio_url="https://example.com/episode1.mp3")

    # Test the episode_number attribute of the podcast episode
    assert episode.episode_number == None

def test_podcastepisode_episode_number():
    # Create a podcast episode object with an episode number
    episode = PodcastEpisode(title="Episode 1", description="Episode 1 description", audio_url="https://example.com/episode1.mp3", episode_number=1)

    # Test the episode_number attribute of the podcast episode
    assert episode.episode_number == 1

def test_podcastepisode_episode_number_invalid():
    # Create a podcast episode object with an invalid episode number
    with pytest.raises(ValueError):
        episode = PodcastEpisode(title="Episode 1", description="Episode 1 description", audio_url="https://example.com/episode1.mp3", episode_number="one")

