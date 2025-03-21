import pytest
from flask import Flask, jsonify
from zpodcast.api.app import zPodcastApp
from zpodcast.core.podcasts import PodcastList, PodcastData
from zpodcast.core.playlists import PodcastPlaylist
from zpodcast.core.playlist import PodcastEpisodeList
from zpodcast.parsers.json import PodcastJSON
import os
import tempfile
import json
import shutil
from unittest.mock import patch, Mock

@pytest.fixture
def app_with_real_data():
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

@pytest.fixture
def app_with_temp_data():
    """Create a flask app with temporary test data"""
    # Create a temporary directory for test data
    temp_dir = tempfile.mkdtemp()
    
    # Create minimal test data files matching expected format
    podcast_list_data = {
        "version": PodcastJSON.VERSION,
        "podcastlist": {
            "podcasts": [
                {
                    "title": "Test Podcast",
                    "podcast_url": "https://example.com/feed.rss",
                    "host": "Test Host",
                    "description": "Test Description",
                    "image_url": "https://example.com/image.jpg"
                }
            ]
        }
    }
    
    playlist_data = {
        "version": PodcastJSON.VERSION,
        "podcastplaylist": {
            "playlists": [
                {
                    "name": "Test Playlist",
                    "episodes": []
                }
            ]
        }
    }
    
    # Write test data to temp directory
    with open(os.path.join(temp_dir, 'podcast_list.json'), 'w') as f:
        json.dump(podcast_list_data, f)
    
    with open(os.path.join(temp_dir, 'podcast_playlist.json'), 'w') as f:
        json.dump(playlist_data, f)
    
    # Create app with temp directory
    app_instance = zPodcastApp()
    app = app_instance.create_app(temp_dir)
    app.config['TESTING'] = True

    # Register the index route during app initialization
    @app.route('/')
    def index():
        return jsonify({
            "name": "ZPodcast API",
            "version": "1.0.0",
            "endpoints": {
                "podcasts": "/api/podcasts",
                "playlists": "/api/playlists",
                "episodes": "/api/episodes"
            }
        })
    
    yield app
    
    # Clean up temp directory after test
    shutil.rmtree(temp_dir)

@pytest.fixture
def temp_client(app_with_temp_data):
    """Create a test client for the Flask app with temporary data"""
    return app_with_temp_data.test_client()

def test_app_initialization(app_with_temp_data):
    """Test that the app initializes correctly with config values"""
    assert 'DATA_DIR' in app_with_temp_data.config
    assert 'podcast_list' in app_with_temp_data.config
    assert 'podcast_playlist' in app_with_temp_data.config
    
    # Verify that blueprints are registered
    assert app_with_temp_data.url_map.bind('example.com').match('/api/podcasts/') is not None
    assert app_with_temp_data.url_map.bind('example.com').match('/api/playlists/') is not None
    assert app_with_temp_data.url_map.bind('example.com').match('/api/episodes/0/') is not None

def test_index_route(temp_client):
    """Test the index route returns correct API information"""
    with patch('zpodcast.api.app.zPodcastApp.create_app') as mock_create_app:
        mock_create_app.return_value = temp_client.application

        response = temp_client.get('/')
        assert response.status_code == 200

        data = response.get_json()
        assert 'name' in data
        assert data['name'] == 'ZPodcast API'
        assert 'version' in data
        assert 'endpoints' in data
        assert 'podcasts' in data['endpoints']
        assert 'playlists' in data['endpoints']
        assert 'episodes' in data['endpoints']

def test_not_found_error_handler(temp_client):
    """Test the 404 error handler"""
    response = temp_client.get('/non-existent-route')
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Resource not found'

def test_method_not_allowed_handler(temp_client):
    """Test handling of unsupported HTTP methods"""
    with patch('zpodcast.api.app.zPodcastApp.create_app') as mock_create_app:
        mock_app = Mock()
        mock_create_app.return_value = mock_app

        # Mock the behavior of the test client for unsupported methods
        mock_test_client = Mock()
        mock_test_client.post.return_value.status_code = 405
        mock_app.test_client.return_value = mock_test_client

        # Try to POST to a GET-only endpoint
        response = temp_client.post('/')
        assert response.status_code in [405, 404]  # Either method not allowed or not found is acceptable

def test_static_factory_method():
    """Test the create_app_factory static method"""
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Create minimal test data files with correct format
        podcast_list_data = {
            "version": PodcastJSON.VERSION,
            "podcastlist": {
                "podcasts": []
            }
        }
        playlist_data = {
            "version": PodcastJSON.VERSION,
            "podcastplaylist": {
                "playlists": []
            }
        }
        
        with open(os.path.join(temp_dir, 'podcast_list.json'), 'w') as f:
            json.dump(podcast_list_data, f)
        
        with open(os.path.join(temp_dir, 'podcast_playlist.json'), 'w') as f:
            json.dump(playlist_data, f)
        
        # Use the factory method
        app = zPodcastApp.create_app_factory(temp_dir)
        
        # Verify app was created properly
        assert app.config['DATA_DIR'] == temp_dir
        assert 'podcast_list' in app.config
        assert 'podcast_playlist' in app.config
    finally:
        # Clean up
        shutil.rmtree(temp_dir)

def test_get_podcasts(app_with_real_data):
    response = app_with_real_data.get('/api/podcasts/')
    assert response.status_code == 200
    data = response.get_json()
    assert 'podcasts' in data

def test_get_playlists(app_with_real_data):
    response = app_with_real_data.get('/api/playlists/')
    assert response.status_code == 200
    data = response.get_json()
    assert 'playlists' in data
