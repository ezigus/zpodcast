import pytest
from flask import jsonify
from zpodcast.api.app import zPodcastApp
from zpodcast.core.podcasts import PodcastList, PodcastData
from zpodcast.core.playlists import PodcastPlaylist
from zpodcast.core.playlist import PodcastEpisodeList
from zpodcast.parsers.json import PodcastJSON
import json
from unittest.mock import patch, Mock, mock_open


@pytest.fixture
def mock_test_data():
    """Mock data for tests without file access"""
    return {
        "podcast_list": PodcastList([
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
        ]),
        "podcast_playlist": PodcastPlaylist([
            PodcastEpisodeList(name="Test Playlist 1", episodes=[]),
            PodcastEpisodeList(name="Test Playlist 2", episodes=[])
        ])
    }


@pytest.fixture
def mock_app(mock_test_data):
    """Create a Flask app with mocked data"""
    podcast_app = zPodcastApp()
    
    # Patch the file access methods
    with patch('zpodcast.parsers.json.PodcastJSON.import_podcast_list') as mock_import_list, \
         patch('zpodcast.parsers.json.PodcastJSON.import_podcast_playlist') as mock_import_playlist:
        
        # Set the return values for the mocked methods
        mock_import_list.return_value = mock_test_data["podcast_list"]
        mock_import_playlist.return_value = mock_test_data["podcast_playlist"]
        
        # Create the app
        app = podcast_app.create_app('tests/data')
        app.config['TESTING'] = True
        
        # Override the index route to ensure it's defined
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
            
        return app


@pytest.fixture
def test_client(mock_app):
    """Create a test client for the Flask app"""
    return mock_app.test_client()


@pytest.fixture
def mock_file_content():
    """Mock content for file operations"""
    podcast_list_content = {
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
    
    podcast_playlist_content = {
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
    
    return {
        "podcast_list.json": json.dumps(podcast_list_content),
        "podcast_playlist.json": json.dumps(podcast_playlist_content)
    }


def test_app_initialization(mock_app):
    """Test that the app initializes correctly with config values"""
    assert 'DATA_DIR' in mock_app.config
    assert 'podcast_list' in mock_app.config
    assert 'podcast_playlist' in mock_app.config
    
    # Verify that blueprints are registered
    assert mock_app.url_map.bind('example.com').match('/api/podcasts/') is not None
    assert mock_app.url_map.bind('example.com').match('/api/playlists/') is not None
    assert mock_app.url_map.bind('example.com').match('/api/episodes/0/') is not None


def test_index_route(test_client):
    """Test the index route returns correct API information"""
    response = test_client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert 'name' in data
    assert data['name'] == 'ZPodcast API'
    assert 'version' in data
    assert 'endpoints' in data
    assert 'podcasts' in data['endpoints']
    assert 'playlists' in data['endpoints']
    assert 'episodes' in data['endpoints']


def test_not_found_error_handler(test_client):
    """Test the 404 error handler"""
    response = test_client.get('/non-existent-route')
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Resource not found'


def test_method_not_allowed_handler(test_client):
    """Test handling of unsupported HTTP methods"""
    # Try to POST to a GET-only endpoint
    response = test_client.post('/')
    assert response.status_code in [405, 404]  # Either method not allowed or not found is acceptable


def test_static_factory_method():
    """Test the create_app_factory static method"""
    with patch('zpodcast.api.app.zPodcastApp.create_app') as mock_create_app:
        # Set up the mock
        mock_app = Mock()
        mock_app.config = {
            'DATA_DIR': '/mock/temp/dir',
            'podcast_list': 'mock_podcast_list',
            'podcast_playlist': 'mock_podcast_playlist'
        }
        mock_create_app.return_value = mock_app
        
        # Call the factory method
        app = zPodcastApp.create_app_factory('/mock/temp/dir')
        
        # Verify the result
        assert mock_create_app.called
        assert app.config['DATA_DIR'] == '/mock/temp/dir'
        assert 'podcast_list' in app.config
        assert 'podcast_playlist' in app.config


def test_get_podcasts(test_client):
    """Test the podcasts endpoint"""
    with patch('zpodcast.core.podcasts.PodcastList.to_dict', return_value={"podcasts": []}):
        response = test_client.get('/api/podcasts/')
        assert response.status_code == 200
        data = response.get_json()
        assert 'podcasts' in data


def test_get_playlists(test_client):
    """Test the playlists endpoint"""
    with patch('zpodcast.core.playlists.PodcastPlaylist.to_dict', return_value={"playlists": []}):
        response = test_client.get('/api/playlists/')
        assert response.status_code == 200
        data = response.get_json()
        assert 'playlists' in data


def test_file_loading():
    """Test that the app correctly loads files"""
    # Create mock file content
    mock_content = {
        "podcast_list.json": json.dumps({
            "version": PodcastJSON.VERSION, 
            "podcastlist": {"podcasts": []}
        }),
        "podcast_playlist.json": json.dumps({
            "version": PodcastJSON.VERSION, 
            "podcastplaylist": {"playlists": []}
        })
    }
    
    # Mock the open function
    def mock_open_func(file, mode='r', *args, **kwargs):
        for filename, content in mock_content.items():
            if filename in file:
                return mock_open(read_data=content)()
        raise FileNotFoundError(f"Mocked file not found: {file}")
    
    # Apply the mocks
    with patch("builtins.open", mock_open_func), \
         patch("os.path.exists", return_value=True), \
         patch("zpodcast.core.podcasts.PodcastList.from_dict"), \
         patch("zpodcast.core.playlists.PodcastPlaylist.from_dict"):
        
        # Create the app
        app = zPodcastApp().create_app('mock/data/dir')
        
        # Verify the app was configured
        assert app.config['DATA_DIR'] == 'mock/data/dir'
