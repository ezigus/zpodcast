import pytest
import dataclasses
from unittest.mock import Mock
from zpodcast.podcastdata import PodcastData
from zpodcast.podcastlist import PodcastList


lTitle="My Podcast"
lHost="John Doe"
lDescription="This is a podcast"


class MockPodcastList:
    pass

episodes = MockPodcastList()

lPodcastURL = "http://example.com/podcast.rss"
lImageURL = "http://example.com/image.jpg"

"""
tests to validate that the class is a dataclass
"""
def test_podcastdata_is_dataclass():
    assert dataclasses.is_dataclass(PodcastData) 



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
test host attribute
"""
def test_host_valid():
    podcast_data = PodcastData(
        title=lTitle,
        podcast_url=lPodcastURL,
        host=lHost,
        description=lDescription,
        episodes=episodes,
        podcast_priority=5,
        image_url=lImageURL
    )

    assert podcast_data.host == lHost
    
def test_host_invalid_int():
    podcast_data = PodcastData(
            title=lTitle,
            podcast_url=lPodcastURL,
            host=5,
            description=lDescription,
            episodes=episodes,
            podcast_priority=5,
            image_url=lImageURL
        )
    assert podcast_data.host == ""

def test_host_invalid_none():
    podcast_data = PodcastData(
        title=lTitle,
        podcast_url=lPodcastURL,
        host=None,
        description=lDescription,
        episodes=episodes,
        podcast_priority=5,
        image_url=lImageURL
    )

    assert podcast_data.host == ""

def test_host_invalid_empty():
    podcast_data = PodcastData(
        title=lTitle,
        podcast_url=lPodcastURL,
        host="",
        description=lDescription,
        episodes=episodes,
        podcast_priority=5,
        image_url=lImageURL
    )

    assert podcast_data.host == ""

"""
test description attribute
"""
def test_description_valid():
    podcast_data = PodcastData(
        title=lTitle,
        podcast_url=lPodcastURL,
        host=lHost,
        description=lDescription,
        episodes=episodes,
        podcast_priority=5,
        image_url=lImageURL
    )

    assert podcast_data.description == lDescription  # Description is set correctly

def test_description_invalid_int():
    podcast_data = PodcastData(
        title=lTitle,
        podcast_url=lPodcastURL,
        host=lHost,
        description=5,
        episodes=episodes,
        podcast_priority=5,
        image_url=lImageURL
    )
    assert podcast_data.description == ""  
        
def test_description_invalid_none():
    podcast_data = PodcastData(
        title=lTitle,
        podcast_url=lPodcastURL,
        host=lHost,
        description=None,
        episodes=episodes,
        podcast_priority=5,
        image_url=lImageURL
    )

    assert podcast_data.description == ""  # Description should be set to an empty string
    
    

""" 
testing the clamp_priority method 
"""
def test_priority_valid():
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

def test_priority_invalid_high():
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

def test_priority_invalid_low():
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

def test_priority_invalid_value():
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
testing episodes attributes are set correctly
"""
def test_podcasmockt_episodes_valid(monkeypatch):
    episodes = Mock(spec=PodcastList)
    podcast_data = PodcastData(
        title=lTitle,
        podcast_url=lPodcastURL,
        host=lHost,
        episodes=episodes,
        description=lDescription,
        podcast_priority=5,
        image_url=lImageURL
    )

    
    print(podcast_data.episodes)
    assert podcast_data.episodes == episodes  # Episodes are set correctly

def test_podcast_episodes_invalid_int():
    podcast_data = PodcastData(
        title=lTitle,
        podcast_url=lPodcastURL,
        host=lHost,
        episodes=5,
        description=lDescription,
        podcast_priority=5,
        image_url=lImageURL
    )

    assert podcast_data.episodes == []  # Episodes should be set to an empty list
    
def test_podcast_episodes_invalid_none():
    podcast_data = PodcastData(
        title=lTitle,
        podcast_url=lPodcastURL,
        host=lHost,
        episodes=None,
        description=lDescription,
        podcast_priority=5,
        image_url=lImageURL
    )

    assert podcast_data.episodes == []  # Episodes should be set to an empty list

def test_podcast_episodes_invalid_empty():
    podcast_data = PodcastData(
        title=lTitle,
        podcast_url=lPodcastURL,
        host=lHost,
        episodes=[],
        description=lDescription,
        podcast_priority=5,
        image_url=lImageURL
    )

    assert podcast_data.episodes == []  # Episodes should be set to an empty list

def test_podcast_episodes_invalid_string():
    podcast_data = PodcastData(
        title=lTitle,
        podcast_url=lPodcastURL,
        host=lHost,
        episodes="invalid",
        description=lDescription,
        podcast_priority=5,
        image_url=lImageURL
    )

    assert podcast_data.episodes == []  # Episodes should be set to an empty list

"""
   testing the validate_image_url method
"""
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