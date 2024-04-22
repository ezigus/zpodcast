import pytest
from zpodcast.podcastdata import PodcastData
from zpodcast.podcastepisode import PodcastEpisode


lTitle="My Podcast"
lHost="John Doe"
lDescription="This is a podcast"

 

episodes = [
        PodcastEpisode(title="Episode 1", description="Episode 1 description", audio_url="http://example.com/audio.mp3", pub_date="Mon, 11 Apr 2016 15:00:00 +0100"),
        PodcastEpisode(title="Episode 1", description="Episode 1 description", audio_url="http://example.com/audio.mp3", pub_date="Mon, 13 Apr 2016 15:00:00 +0100"),        
        PodcastEpisode(title="Episode 1", description="Episode 1 description", audio_url="http://example.com/audio.mp3", pub_date="Mon, 15 Apr 2016 15:00:00 +0100"),        
    ]
lPodcastURL = "http://example.com/podcast.rss"
lImageURL = "http://example.com/image.jpg"

"""
Testing title attribute
"""
def test_title():
    podcast_data = PodcastData(
        title=lTitle,
        podcast_url=lPodcastURL,
        host=lHost,
        description=lDescription,
        episodes=episodes,
        podcast_priority=5,
        image_url=lImageURL
    )

    assert podcast_data.title == lTitle  # Title is set correctly

def test_notitle():
    with pytest.raises(TypeError):
        podcast_data = PodcastData(
            podcast_url="http://example.com/podcast.rss",
            host=lHost,
            description=lDescription,
            episodes=episodes,
            podcast_priority=5,
            image_url=lImageURL
        )

def test_title_int():
    with pytest.raises(ValueError, match="^Invalid title$"):
        podcast_data = PodcastData(
            title=5,
            podcast_url=lPodcastURL,
            host=lHost,
            description=lDescription,
            episodes=episodes,
            podcast_priority=5,
            image_url=lImageURL
        )

"""
tests for podcast url
"""
def test_podcast_url_valid():
    podcast_data = PodcastData(
        title=lTitle,
        podcast_url=lPodcastURL,
        host=lHost,
        description=lDescription,
        episodes=episodes,
        podcast_priority=5,
        image_url=lImageURL
    )

    assert podcast_data.podcast_url == lPodcastURL  # Podcast URL is set correctly
    
def test_podcast_url_invalid_int():
    with pytest.raises(ValueError, match="^Invalid podcast URL$"):
        podcast_data = PodcastData(
            title=lTitle,
            podcast_url=5,
            host=lHost,
            description=lDescription,
            episodes=episodes,
            podcast_priority=5,
            image_url=lImageURL
        )

def test_podcast_url_invalid_none():
    with pytest.raises(ValueError, match="^Invalid podcast URL$"):
        podcast_data = PodcastData(
            title=lTitle,
            podcast_url=None,
            host=lHost,
            description=lDescription,
            episodes=episodes,
            podcast_priority=5,
            image_url=lImageURL
        )

def test_podcast_url_invalid_empty():
    with pytest.raises(ValueError, match="^Invalid podcast URL$"):
        podcast_data = PodcastData(
            title=lTitle,
            podcast_url="",
            host=lHost,
            description=lDescription,
            episodes=episodes,
            podcast_priority=5,
            image_url=lImageURL
        )
        
def test_podcast_url_invalid_url():
    with pytest.raises(ValueError, match="^Invalid podcast URL$"):
        podcast_data = PodcastData(
            title=lTitle,
            podcast_url="invalid",
            host=lHost,
            description=lDescription,
            episodes=episodes,
            podcast_priority=5,
            image_url=lImageURL
        )

""" 
testing the clamp_priority method 
"""
def test_clamp_priority_valid():
    podcast_data = PodcastData(
        title=lTitle,
        podcast_url=lPodcastURL,
        host=lHost,
        description=lDescription,
        episodes=episodes,
        podcast_priority=5,
        image_url=lImageURL
    )
    assert podcast_data.podcast_priority == 5  # Priority should remain unchanged

def test_clamp_priority_invalid_high():
    podcast_data = PodcastData(
        title=lTitle,
        podcast_url=lPodcastURL,
        host=lHost,
        description=lDescription,
        episodes=episodes,
        podcast_priority=25,
        image_url=lImageURL
    )
    
    assert podcast_data.podcast_priority == 10  # Priority should be clamped to 10

def test_clamp_priority_invalid_low():
    podcast_data = PodcastData(
        title=lTitle,
        podcast_url=lPodcastURL,
        host=lHost,
        description=lDescription,
        episodes=episodes,
        podcast_priority=-25,
        image_url=lImageURL
    )    
    assert podcast_data.podcast_priority == -10  # Priority should be clamped to -10

def test_clamp_priority_invalid_value():
    podcast_data = PodcastData(
        title=lTitle,
        podcast_url=lPodcastURL,
        host=lHost,
        description=lDescription,
        podcast_priority="invalid",
        image_url=lImageURL
    )    
    assert podcast_data.podcast_priority == 0  # Priority should be set to 0

"""
   testing the validate_image_url method
"""

def test_validate_image_url():
    podcast_data = PodcastData(
        title=lTitle,
        podcast_url=lPodcastURL,
        host=lHost,
        description=lDescription,
        podcast_priority=5,
        image_url=lImageURL
    )

    assert podcast_data.validate_image_url()  # Image URL is valid

def test_image_url():
    podcast_data = PodcastData(
        title=lTitle,
        podcast_url=lPodcastURL,
        host=lHost,
        description=lDescription,
        podcast_priority=5,
        image_url=lImageURL
    )

    assert podcast_data.image_url == lImageURL  # Image URL is set correctly


def test_podcast_data_attributes():
    podcast_data = PodcastData(
        title=lTitle,
        podcast_url=lPodcastURL,
        host=lHost,
        episodes=episodes,
        description=lDescription,
        podcast_priority=5,
        image_url=lImageURL
    )

    assert podcast_data.title == lTitle
    assert podcast_data.host == lHost
    assert podcast_data.description == lDescription
    assert podcast_data.episodes == episodes
    assert podcast_data.podcast_priority == 5
    assert podcast_data._image_url == lImageURL
