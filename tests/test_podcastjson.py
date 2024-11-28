import os
import json
import pytest
from zpodcast.podcastjson import PodcastJSON
from zpodcast.podcastlist import PodcastList
from zpodcast.podcastplaylist import PodcastPlaylist
from zpodcast.podcastdata import PodcastData
from zpodcast.podcastepisodelist import PodcastEpisodeList
from zpodcast.podcastepisode import PodcastEpisode

@pytest.fixture
def sample_podcast_list():
    episodes = PodcastEpisodeList(name="Test Episode List", episodes=[
        PodcastEpisode(title="Episode 1", audio_url="https://example.com/episode1.mp3"),
        PodcastEpisode(title="Episode 2", audio_url="https://example.com/episode2.mp3")
    ])
    podcast1 = PodcastData(
        title="Test Podcast 1",
        podcast_url="http://example.com/podcast1.rss",
        host="John Doe",
        description="This is a test podcast 1",
        episodes=episodes,
        podcast_priority=5,
        image_url="http://example.com/image1.jpg"
    )
    podcast2 = PodcastData(
        title="Test Podcast 2",
        podcast_url="http://example.com/podcast2.rss",
        host="Jane Doe",
        description="This is a test podcast 2",
        episodes=episodes,
        podcast_priority=5,
        image_url="http://example.com/image2.jpg"
    )
    return PodcastList([podcast1, podcast2])

@pytest.fixture
def sample_podcast_playlist():
    episodes1 = PodcastEpisodeList(name="Test Episode List 1", episodes=[
        PodcastEpisode(title="Episode 1", audio_url="https://example.com/episode1.mp3"),
        PodcastEpisode(title="Episode 2", audio_url="https://example.com/episode2.mp3")
    ])
    episodes2 = PodcastEpisodeList(name="Test Episode List 2", episodes=[
        PodcastEpisode(title="Episode 3", audio_url="https://example.com/episode3.mp3"),
        PodcastEpisode(title="Episode 4", audio_url="https://example.com/episode4.mp3")
    ])
    return PodcastPlaylist([episodes1, episodes2])

def test_export_podcast_list(sample_podcast_list):
    filename = "test_podcast_list.json"
    PodcastJSON.export_podcast_list(sample_podcast_list, filename)
    assert os.path.exists(filename)
    with open(filename, 'r') as f:
        data = json.load(f)
        assert data["version"] == "0.1"
        assert "podcastlist" in data
    os.remove(filename)

def test_import_podcast_list(sample_podcast_list):
    filename = "test_podcast_list.json"
    PodcastJSON.export_podcast_list(sample_podcast_list, filename)
    imported_podcast_list = PodcastJSON.import_podcast_list(filename)
    assert imported_podcast_list.to_dict() == sample_podcast_list.to_dict()
    os.remove(filename)

def test_export_podcast_playlist(sample_podcast_playlist):
    filename = "test_podcast_playlist.json"
    PodcastJSON.export_podcast_playlist(sample_podcast_playlist, filename)
    assert os.path.exists(filename)
    with open(filename, 'r') as f:
        data = json.load(f)
        assert data["version"] == "0.1"
        assert "podcastplaylist" in data
    os.remove(filename)

def test_import_podcast_playlist(sample_podcast_playlist):
    filename = "test_podcast_playlist.json"
    PodcastJSON.export_podcast_playlist(sample_podcast_playlist, filename)
    imported_podcast_playlist = PodcastJSON.import_podcast_playlist(filename)
    assert imported_podcast_playlist.to_dict() == sample_podcast_playlist.to_dict()
    os.remove(filename)