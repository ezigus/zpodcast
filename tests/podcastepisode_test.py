import pytest
from email.utils import parsedate_tz, mktime_tz
from zpodcast.podcastepisode import PodcastEpisode

   
def test_podcastepisode_title():
    # Create a podcast episode object
    episode = PodcastEpisode(title="Episode 1", description="Episode 1 description", audio_url="https://example.com/episode1.mp3", duration=1800)

    # Test the title attribute of the podcast episode
    assert episode.title == "Episode 1"

def test_podcastepisode_duration():
    # Create a podcast episode object
    episode = PodcastEpisode(title="Episode 1", description="Episode 1 description", audio_url="https://example.com/episode1.mp3", duration=1800)

    # Test the duration attribute of the podcast episode
    assert episode.duration == 1800
    
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
    
    