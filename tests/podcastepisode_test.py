import pytest
from zpodcast.podcastepisode import PodcastEpisode

def test_podcastepisode():
    # Create a podcast episode object
    episode = PodcastEpisode(title="Episode 1", description="Episode 1 description", audio_url="https://example.com/episode1.mp3", duration=1800)

    # Test the attributes of the podcast episode
    assert episode.title == "Episode 1"
    assert episode.duration == 1800
    assert episode.description == "Episode 1 description"
    assert episode.audio_url == "https://example.com/episode1.mp3"
    
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