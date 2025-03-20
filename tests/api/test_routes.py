import pytest
from flask import Flask
from zpodcast.api.routes import register_podcast_routes, register_podcast_playlist_routes
from zpodcast.core.podcasts import PodcastList, PodcastData
from zpodcast.core.playlists import PodcastPlaylist
from zpodcast.core.playlist import PodcastEpisodeList

@pytest.fixture
def app():
    app = Flask(__name__)
    
    # Set up test data
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

    # Register routes
    register_podcast_routes(app)
    register_podcast_playlist_routes(app)

    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_register_podcast_routes(client):
    """Test that podcast routes are registered correctly"""
    response = client.get('/podcasts')
    assert response.status_code == 200
    data = response.get_json()
    assert 'podcasts' in data
    assert len(data['podcasts']) == 2
    assert data['podcasts'][0]['title'] == "Test Podcast 1"
    assert data['podcasts'][1]['title'] == "Test Podcast 2"

def test_register_podcast_playlist_routes(client):
    """Test that playlist routes are registered correctly"""
    response = client.get('/playlists')
    assert response.status_code == 200
    data = response.get_json()
    assert 'playlists' in data
    assert len(data['playlists']) == 2
    assert data['playlists'][0]['name'] == "Test Playlist 1"
    assert data['playlists'][1]['name'] == "Test Playlist 2"

def test_podcast_routes_with_empty_list(client):
    """Test podcast routes with an empty podcast list"""
    client.application.config['podcast_list'] = PodcastList([])
    response = client.get('/podcasts')
    assert response.status_code == 200
    data = response.get_json()
    assert 'podcasts' in data
    assert len(data['podcasts']) == 0

def test_playlist_routes_with_empty_list(client):
    """Test playlist routes with an empty playlist"""
    client.application.config['podcast_playlist'] = PodcastPlaylist([])
    response = client.get('/playlists')
    assert response.status_code == 200
    data = response.get_json()
    assert 'playlists' in data
    assert len(data['playlists']) == 0 