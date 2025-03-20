import pytest
from flask import Flask
from zpodcast.api.blueprints.episodes import episodes_bp
from zpodcast.core.podcasts import PodcastList
from zpodcast.core.podcast import PodcastData
from zpodcast.core.episode import PodcastEpisode
from zpodcast.core.playlist import PodcastEpisodeList
from datetime import datetime, timedelta

@pytest.fixture
def test_episode_data():
    """Create test episode data for testing"""
    now = datetime.now()
    return [
        PodcastEpisode(
            title="Test Episode 1",
            audio_url="http://example.com/episode1.mp3",
            description="This is test episode 1",
            pub_date=now - timedelta(days=1),
            duration=1800,  # 30 minutes
            episode_number=1,
            image_url="http://example.com/episode1.jpg"
        ),
        PodcastEpisode(
            title="Test Episode 2",
            audio_url="http://example.com/episode2.mp3",
            description="This is test episode 2",
            pub_date=now - timedelta(days=2),
            duration=3600,  # 60 minutes
            episode_number=2,
            image_url="http://example.com/episode2.jpg"
        )
    ]

@pytest.fixture
def test_podcast_data(mocker, test_episode_data):
    """Create test podcast data with episodes for testing"""
    # Mock RSSPodcastParser to prevent actual RSS fetching
    mocker.patch('zpodcast.parsers.rss.RSSPodcastParser.get_episodes', return_value=[])
    mocker.patch('zpodcast.parsers.rss.RSSPodcastParser.get_rss_metadata', return_value={
        "title": "Test Podcast", 
        "description": "This is a test podcast", 
        "author": "Test Author", 
        "image": "http://example.com/image.jpg"
    })
    
    # Create test data with pre-populated episodes
    episode_list = PodcastEpisodeList(
        name="Test Podcast episode list",
        episodes=test_episode_data
    )
    
    # This is important - we need to patch the populate_episodes_from_feed method
    # to prevent it from overwriting our test episodes
    mocker.patch('zpodcast.core.podcast.PodcastData.populate_episodes_from_feed')
    
    return [
        PodcastData(
            title="Test Podcast",
            podcast_url="http://example.com/podcast.rss",
            host="Test Author",
            description="This is a test podcast",
            episodelists=[episode_list],
            podcast_priority=5,
            image_url="http://example.com/image.jpg"
        )
    ]

@pytest.fixture
def app(mocker, test_podcast_data):
    """Set up a Flask app with the episodes blueprint registered"""
    app = Flask(__name__)
    
    # Create a consistent test PodcastList
    podcast_list = PodcastList(test_podcast_data)
    
    # Mock the get_instance method
    mocker.patch('zpodcast.core.podcasts.PodcastList.get_instance', 
                return_value=podcast_list)
    mocker.patch('zpodcast.api.blueprints.episodes.PodcastList.get_instance', 
                return_value=podcast_list)
    
    # Register blueprint
    app.register_blueprint(episodes_bp, url_prefix='/api/episodes')
    
    return app

@pytest.fixture
def client(app):
    """Create a test client for the Flask app"""
    return app.test_client()

def test_get_episodes(client):
    """Test getting all episodes for a podcast"""
    response = client.get('/api/episodes/0/')
    assert response.status_code == 200
    data = response.get_json()
    assert 'episodes' in data
    assert len(data['episodes']) == 2
    assert data['episodes'][0]['title'] == "Test Episode 1"
    assert data['episodes'][1]['title'] == "Test Episode 2"

def test_get_episodes_podcast_not_found(client):
    """Test getting episodes for a non-existent podcast"""
    response = client.get('/api/episodes/999/')
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Podcast not found'

def test_get_episode(client):
    """Test getting a specific episode"""
    response = client.get('/api/episodes/0/0/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == "Test Episode 1"
    assert data['audio_url'] == "http://example.com/episode1.mp3"
    assert data['duration'] == 1800
    assert data['episode_number'] == 1

def test_get_episode_podcast_not_found(client):
    """Test getting an episode from a non-existent podcast"""
    response = client.get('/api/episodes/999/0/')
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Podcast not found'

def test_get_episode_not_found(client):
    """Test getting a non-existent episode"""
    response = client.get('/api/episodes/0/999/')
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Episode not found'