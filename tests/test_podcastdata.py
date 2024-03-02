import pytest
from zpodcast.podcastdata import PodcastData
from zpodcast.podcastepisode import PodcastEpisode


""" 
testing the clamp_priority method 
"""
def test_clamp_priority_valid():
    episodes = [
        PodcastEpisode("Episode 1", "2022-01-01","http://example.com/audio.mp3"),
        PodcastEpisode("Episode 2", "2022-01-08","http://example.com/audio.mp3"),
        PodcastEpisode("Episode 3", "2022-01-15","http://example.com/audio.mp3")
    ]
    podcast_data = PodcastData(
        "My Podcast",
        "John Doe",
        "A podcast about something",
        episodes,
        priority=5,
        _image_url="https://example.com/image.jpg"
    )

    podcast_data.clamp_priority()
    assert podcast_data.priority == 5  # Priority should remain unchanged

def test_clamp_priority_invalid_high():
    episodes = [
        PodcastEpisode("Episode 1", "2022-01-01","http://example.com/audio.mp3"),
        PodcastEpisode("Episode 2", "2022-01-08","http://example.com/audio.mp3"),
        PodcastEpisode("Episode 3", "2022-01-15","http://example.com/audio.mp3")
    ]
    podcast_data = PodcastData(
        "My Podcast",
        "John Doe",
        "A podcast about something",
        episodes,
        priority=5,
        _image_url="https://example.com/image.jpg"
    )
    
    podcast_data.priority = 15
    podcast_data.clamp_priority()
    assert podcast_data.priority == 10  # Priority should be clamped to 10

def test_clamp_priority_invalid_low():
    episodes = [
        PodcastEpisode("Episode 1", "2022-01-01","http://example.com/audio.mp3"),
        PodcastEpisode("Episode 2", "2022-01-08","http://example.com/audio.mp3"),
        PodcastEpisode("Episode 3", "2022-01-15","http://example.com/audio.mp3")
    ]
    podcast_data = PodcastData(
        "My Podcast",
        "John Doe",
        "A podcast about something",
        episodes,
        priority=5,
        _image_url="https://example.com/image.jpg"
    )    
    podcast_data.priority = -20
    podcast_data.clamp_priority()
    assert podcast_data.priority == -10  # Priority should be clamped to -10

"""
   testing the validate_image_url method
"""

def test_validate_image_url():
    episodes = [
        PodcastEpisode("Episode 1", "2022-01-01","http://example.com/audio.mp3"),
        PodcastEpisode("Episode 2", "2022-01-08","http://example.com/audio.mp3"),
        PodcastEpisode("Episode 3", "2022-01-15","http://example.com/audio.mp3")
    ]
    podcast_data = PodcastData(
        "My Podcast",
        "John Doe",
        "A podcast about something",
        episodes,
        priority=5,
        _image_url="https://example.com/image.jpg"
    )

    assert podcast_data.validate_image_url()  # Image URL is valid

    podcast_data._image_url = "invalid_url"
    assert not podcast_data.validate_image_url()  # Image URL is invalid

def test_image_url():
    episodes = [
        PodcastEpisode("Episode 1", "2022-01-01","http://example.com/audio.mp3"),
        PodcastEpisode("Episode 2", "2022-01-08","http://example.com/audio.mp3"),
        PodcastEpisode("Episode 3", "2022-01-15","http://example.com/audio.mp3")
    ]
    podcast_data = PodcastData(
        "My Podcast",
        "John Doe",
        "A podcast about something",
        episodes,
        priority=5,
        _image_url="https://example.com/image.jpg"
    )

    assert podcast_data.image_url == "https://example.com/image.jpg"  # Image URL is set correctly

    podcast_data.image_url = "https://newimage.com/new.jpg"
    assert podcast_data.image_url == "https://newimage.com/new.jpg"  # Image URL is updated correctly

def test_podcast_data_attributes():
    episodes = [
        PodcastEpisode("Episode 1", "2022-01-01","http://example.com/audio.mp3"),
        PodcastEpisode("Episode 2", "2022-01-08","http://example.com/audio.mp3"),
        PodcastEpisode("Episode 3", "2022-01-15","http://example.com/audio.mp3")
    ]
    podcast_data = PodcastData(
        "My Podcast",
        "John Doe",
        "A podcast about something",
        episodes,
        priority=5,
        _image_url="https://example.com/image.jpg"
    )

    assert podcast_data.title == "My Podcast"
    assert podcast_data.host == "John Doe"
    assert podcast_data.description == "A podcast about something"
    assert podcast_data.episodes == episodes
    assert podcast_data.priority == 5
    assert podcast_data._image_url == "https://example.com/image.jpg"
