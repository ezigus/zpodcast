import pytest
from flask import Flask
from zpodcast.api.blueprints.podcasts import podcasts_bp
from zpodcast.core.podcasts import PodcastList
from zpodcast.core.podcast import PodcastData

@pytest.fixture
def test_podcast_data(mocker):
    """Create test podcast data for testing with proper mocking"""
    # Mock RSSPodcastParser to return consistent data matching our test expectations
    mocker.patch('zpodcast.parsers.rss.RSSPodcastParser.get_episodes', return_value=[])
    
    # Mock different metadata for each podcast to match our test expectations
    mock_get_rss_metadata = mocker.patch('zpodcast.parsers.rss.RSSPodcastParser.get_rss_metadata')
    mock_get_rss_metadata.side_effect = [
        {
            "title": "Test Podcast 1", 
            "description": "This is a test podcast 1", 
            "author": "John Doe", 
            "image": "http://example.com/image1.jpg"
        },
        {
            "title": "Test Podcast 2", 
            "description": "This is a test podcast 2", 
            "author": "Jane Doe", 
            "image": "http://example.com/image2.jpg"
        },
        {
            "title": "New Podcast", 
            "description": "This is a new podcast", 
            "author": "New Host", 
            "image": "http://example.com/new.jpg"
        }
    ]
    
    return [
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
    ]

@pytest.fixture
def app(mocker, test_podcast_data):
    """Set up a Flask app with the podcast blueprint registered"""
    app = Flask(__name__)
    
    # Create a consistent test PodcastList
    podcast_list = PodcastList(test_podcast_data)
    
    # Patch the get_instance method in both places it's used
    mocker.patch('zpodcast.core.podcasts.PodcastList.get_instance', 
                return_value=podcast_list)
    mocker.patch('zpodcast.api.blueprints.podcasts.PodcastList.get_instance', 
                return_value=podcast_list)
    
    # Register blueprint
    app.register_blueprint(podcasts_bp, url_prefix='/api/podcasts')
    
    return app

@pytest.fixture
def client(app):
    """Create a test client for the Flask app"""
    return app.test_client()

def test_get_podcasts(client):
    """Test getting all podcasts through the blueprint"""
    response = client.get('/api/podcasts/')
    assert response.status_code == 200
    data = response.get_json()
    assert 'podcasts' in data
    assert len(data['podcasts']) == 2
    assert data['podcasts'][0]['title'] == "Test Podcast 1"
    assert data['podcasts'][1]['title'] == "Test Podcast 2"

def test_get_podcast_by_id(client):
    """Test getting a specific podcast by ID through the blueprint"""
    response = client.get('/api/podcasts/0/')  # First podcast
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == "Test Podcast 1"
    assert data['host'] == "John Doe"

def test_get_podcast_by_id_not_found(client):
    """Test getting a non-existent podcast ID through the blueprint"""
    response = client.get('/api/podcasts/999/')
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Podcast not found'

def test_add_podcast(client, mocker, test_podcast_data):
    """Test adding a new podcast"""
    # Set up the test PodcastList as a mutable fixture that will be modified
    podcast_list = PodcastList(test_podcast_data.copy())
    mocker.patch('zpodcast.api.blueprints.podcasts.PodcastList.get_instance', 
                return_value=podcast_list)
    
    new_podcast = {
        "title": "New Podcast",
        "podcast_url": "http://example.com/new.rss",
        "host": "New Host",
        "description": "This is a new podcast",
        "podcast_priority": 5,
        "image_url": "http://example.com/new.jpg"
    }
    response = client.post('/api/podcasts/', json=new_podcast)
    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == "New Podcast"
    assert data['host'] == "New Host"

def test_add_podcast_no_data(client):
    """Test adding a podcast with no data"""
    response = client.post('/api/podcasts/', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'No data provided'

def test_delete_podcast(client, mocker, test_podcast_data):
    """Test removing a podcast"""
    # Create a fresh podcast list for this test
    podcast_list = PodcastList(test_podcast_data.copy())
    
    # Store information about the podcast we're going to delete
    to_delete = podcast_list.get_podcast(0)
    
    # Create a consistent mock that will be used throughout the test
    mock_get_instance = mocker.patch('zpodcast.api.blueprints.podcasts.PodcastList.get_instance',
                return_value=podcast_list)
    
    # First verify the podcast exists
    response = client.get('/api/podcasts/0/')
    assert response.status_code == 200
    first_id_data = response.get_json()
    assert first_id_data['title'] == "Test Podcast 1"
    
    # Then delete it
    response = client.delete('/api/podcasts/0/')
    assert response.status_code == 204
    
    # The podcast at index 1 will now be at index 0
    # Verify that index 0 now contains what was previously at index 1
    response = client.get('/api/podcasts/0/')
    assert response.status_code == 200
    new_first_data = response.get_json()
    assert new_first_data['title'] == "Test Podcast 2"
    
    # Verify that the list now has one less podcast
    response = client.get('/api/podcasts/')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['podcasts']) == 1

def test_delete_podcast_not_found(client):
    """Test removing a non-existent podcast"""
    response = client.delete('/api/podcasts/999/')
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Podcast not found'

def test_update_podcast(client, mocker, test_podcast_data):
    """Test updating an existing podcast"""
    # Create a fresh podcast list for this test
    podcast_list = PodcastList(test_podcast_data.copy())
    mocker.patch('zpodcast.api.blueprints.podcasts.PodcastList.get_instance', 
                return_value=podcast_list)
    
    # Setup podcast update data
    update_data = {
        "title": "Updated Podcast Title",
        "description": "This is an updated description",
    }
    
    # Add a mock for the update_podcast method - we'll need to implement this in the PodcastList class
    mocker.patch('zpodcast.core.podcasts.PodcastList.update_podcast', 
                return_value=test_podcast_data[0])
    
    # Call the update endpoint with trailing slash
    response = client.put('/api/podcasts/0/', json=update_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == "Test Podcast 1"  # We're using the mock return value

def test_update_podcast_no_data(client):
    """Test updating a podcast with no data"""
    response = client.put('/api/podcasts/0/', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'No data provided'

def test_update_podcast_not_found(client, mocker):
    """Test updating a non-existent podcast"""
    # Mock the update_podcast method to raise ValueError
    mocker.patch('zpodcast.core.podcasts.PodcastList.update_podcast', 
                side_effect=ValueError("Podcast not found"))
    
    response = client.put('/api/podcasts/999/', json={"title": "Test"})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_update_podcast_non_integer_id(client):
    """Test updating a podcast with a non-integer ID to verify the route only accepts integers"""
    # Flask will return a 404 for routes that don't match the expected pattern
    # This tests that the <int:podcast_id> type converter is working correctly
    response = client.put('/api/podcasts/abc/', json={"title": "Updated Title"})
    assert response.status_code == 404  # Not Found, because the route doesn't match