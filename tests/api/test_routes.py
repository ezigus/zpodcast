import pytest
from flask import Flask
from unittest.mock import patch
from zpodcast.api.routes import register_podcast_routes, register_podcast_playlist_routes

class MockPodcastList:
    def __init__(self, podcasts):
        self._podcasts = podcasts

    def to_dict(self):
        return {'podcasts': self._podcasts}

class MockPodcastPlaylist:
    def __init__(self, playlists):
        self._playlists = playlists

    def to_dict(self):
        return {'playlists': self._playlists}

@pytest.fixture
def app():
    app = Flask(__name__)

    # Use explicit mock objects
    app.config['podcast_list'] = MockPodcastList([
        {'title': "Test Podcast 1"},
        {'title': "Test Podcast 2"}
    ])
    app.config['podcast_playlist'] = MockPodcastPlaylist([
        {'name': "Test Playlist 1"},
        {'name': "Test Playlist 2"}
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

def test_podcast_routes_with_empty_list(client, app):
    """Test podcast routes with an empty podcast list"""
    app.config['podcast_list'] = MockPodcastList([])
    response = client.get('/podcasts')
    assert response.status_code == 200
    data = response.get_json()
    assert 'podcasts' in data
    assert len(data['podcasts']) == 0

def test_playlist_routes_with_empty_list(client, app):
    """Test playlist routes with an empty playlist"""
    app.config['podcast_playlist'] = MockPodcastPlaylist([])
    response = client.get('/playlists')
    assert response.status_code == 200
    data = response.get_json()
    assert 'playlists' in data
    assert len(data['playlists']) == 0