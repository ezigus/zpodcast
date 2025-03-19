import pytest
from flask import Flask, jsonify
from zpodcast.api.app import zPodcastApp
from zpodcast.core.podcasts import PodcastList, PodcastData
from zpodcast.core.playlists import PodcastPlaylist
from zpodcast.core.playlist import PodcastEpisodeList

@pytest.fixture
def client():
    podcast_app = zPodcastApp()
    app = podcast_app.create_app('tests/data')

    # Mock podcast_list and podcast_playlist
    app.config['podcast_list'] = PodcastList([
        PodcastData(
            title="Test Podcast 1",
            podcast_url="http://example.com/podcast1.rss",
            host="John Doe",
            description="This is a test podcast 1",
            episodelists=[],
            podcast_priority=5,
            image_url="http://example.com/image1.jpg"
        ),
        PodcastData(
            title="Test Podcast 2",
            podcast_url="http://example.com/podcast2.rss",
            host="Jane Doe",
            description="This is a test podcast 2",
            episodelists=[],
            podcast_priority=5,
            image_url="http://example.com/image2.jpg"
        )
    ])

    app.config['podcast_playlist'] = PodcastPlaylist([
        PodcastEpisodeList(name="Test Playlist 1", episodes=[]),
        PodcastEpisodeList(name="Test Playlist 2", episodes=[])
    ])

    with app.test_client() as client:
        yield client

def test_get_podcasts(client):
    response = client.get('/api/podcasts')
    assert response.status_code == 200
    data = response.get_json()
    assert 'podcasts' in data

def test_get_playlists(client):
    response = client.get('/api/playlists')
    assert response.status_code == 200
    data = response.get_json()
    assert 'playlists' in data
