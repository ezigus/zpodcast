import pytest
import dataclasses
from zpodcast.podcastdata import PodcastData
from zpodcast.podcastepisodelist import PodcastEpisodeList
from zpodcast.podcastepisode import PodcastEpisode
from datetime import date

lTitle="My Podcast"
lHost="John Doe"
lDescription="This is a podcast"
episode1 = PodcastEpisode(title="Episode 1", audio_url="https://example.com/episode1.mp3")
episode2 = PodcastEpisode(title="Episode 2", audio_url="https://example.com/episode2.mp3")
episodelist1 = PodcastEpisodeList(name="Podcast Episode List1", episodes=[episode1,episode2])
episodelists = [episodelist1]

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
        episodelists=episodelists,
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
            episodelists=episodelists,
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
            episodelists=episodelists,
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
        episodelists=episodelists,
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
            episodelists=episodelists,
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
            episodelists=episodelists,
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
            episodelists=episodelists,
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
            episodelists=episodelists,
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
        episodelists=episodelists,
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
            episodelists=episodelists,
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
        episodelists=episodelists,
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
        episodelists=episodelists,
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
        episodelists=episodelists,
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
        episodelists=episodelists,
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
        episodelists=episodelists,
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
        episodelists=episodelists,
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
        episodelists=episodelists,
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
        episodelists=episodelists,
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
def test_podcast_episodes_valid():
    podcast_data = PodcastData(
        title=lTitle,
        podcast_url=lPodcastURL,
        host=lHost,
        episodelists=episodelists,
        description=lDescription,
        podcast_priority=5,
        image_url=lImageURL
    )

    assert podcast_data.episodelists == episodelists  # Episodes are set correctly

def test_podcast_episodes_invalid_int():
    podcast_data = PodcastData(
        title=lTitle,
        podcast_url=lPodcastURL,
        host=lHost,
        episodelists=5,
        description=lDescription,
        podcast_priority=5,
        image_url=lImageURL
    )

    assert podcast_data.episodelists == []  # Episodes should be set to an empty list
    
def test_podcast_episodes_invalid_none():
    podcast_data = PodcastData(
        title=lTitle,
        podcast_url=lPodcastURL,
        host=lHost,
        episodelists=None,
        description=lDescription,
        podcast_priority=5,
        image_url=lImageURL
    )

    assert podcast_data.episodelists == []  # Episodes should be set to an empty list

def test_podcast_episodes_invalid_empty():
    podcast_data = PodcastData(
        title=lTitle,
        podcast_url=lPodcastURL,
        host=lHost,
        episodelists=[],
        description=lDescription,
        podcast_priority=5,
        image_url=lImageURL
    )
    assert podcast_data.episodelists == []  # Episodes should be set to an empty list

def test_podcast_episodes_invalid_string():
    podcast_data = PodcastData(
        title=lTitle,
        podcast_url=lPodcastURL,
        host=lHost,
        episodelists="invalid",
        description=lDescription,
        podcast_priority=5,
        image_url=lImageURL
    )

    assert podcast_data.episodelists == []  # Episodes should be set to an empty list

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

def test_to_dict():
    podcastepisodelist = PodcastEpisodeList(name="podcastepisodelist1", episodes=[
        PodcastEpisode(title="Episode 1", audio_url="https://example.com/episode1.mp3"),
        PodcastEpisode(title="Episode 2", audio_url="https://example.com/episode2.mp3")
    ])
    
    podcast1 = PodcastData(
        title="Test Podcast 1",
        podcast_url="http://example.com/podcast1.rss",
        host="John Doe",
        description="This is a test podcast 1",
        episodelists=[podcastepisodelist],
        podcast_priority=5,
        image_url="http://example.com/image1.jpg"
    )
    
    podcast_dict = podcast1.to_dict()
  
    assert podcast_dict.get("title") == podcast1.title
    assert podcast_dict.get("podcast_url") == podcast1.podcast_url
    assert podcast_dict.get("host") ==  podcast1.host
    assert podcast_dict.get("description") == podcast1.description
    assert podcast_dict.get("podcast_priority") == podcast1.podcast_priority
    assert podcast_dict.get("image_url") == podcast1.image_url
    print (podcast_dict.get("episodelist"))
    print (podcastepisodelist.to_dict())
    assert podcast_dict.get("episodelists") == podcastepisodelist.to_dict()

def test_from_dict():
    print(f"episodes_lists_dict = {episodelists.to_dict()}")
    podcast_dict = {
        "title": lTitle,
        "podcast_url": lPodcastURL,
        "host": lHost,
        "description": lDescription,
        "episodelists": episodelists.to_dict(),
        "podcast_priority": 5,
        "image_url": lImageURL
    }
    podcast_data = PodcastData.from_dict(podcast_dict)
    
    assert podcast_data.title == lTitle
    assert podcast_data.podcast_url == lPodcastURL
    assert podcast_data.host == lHost
    assert podcast_data.description == lDescription
    assert podcast_data.episodelists == episodelists.to_dict()
    assert podcast_data.podcast_priority == 5
    assert podcast_data.image_url == lImageURL
