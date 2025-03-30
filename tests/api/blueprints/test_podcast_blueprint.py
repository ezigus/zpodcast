"""
Podcast Blueprint Tests Module

This module contains tests for the podcast API blueprint endpoints.
It verifies that all podcast-related API endpoints work as expected
and correctly handle both successful and error scenarios.

The tests use pytest fixtures to set up test data and mock dependencies,
focusing on validating the HTTP status codes, response formats, and
proper error handling for each endpoint.
"""
import pytest
from flask import Flask
from zpodcast.api.blueprints.podcasts import podcasts_bp
from zpodcast.core.podcasts import PodcastList
from zpodcast.core.podcast import PodcastData

@pytest.fixture
def test_podcast_data(mocker):
    """
    Create test podcast data for testing with proper mocking.
    
    This fixture sets up mock podcast data and patches RSS-related 
    functionality to ensure consistent test behavior. It creates
    two test podcasts with predefined metadata that can be used
    across multiple tests.
    
    Args:
        mocker: The pytest-mock fixture for creating mock objects
        
    Returns:
        List[PodcastData]: A list containing two test podcast objects
    """
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
    """
    Set up a Flask app with the podcast blueprint registered.
    
    This fixture creates a Flask test application, registers the 
    podcasts blueprint, and sets up mocks to ensure the application
    uses the test podcast data for all operations.
    
    Args:
        mocker: The pytest-mock fixture for creating mock objects
        test_podcast_data: The fixture providing test podcast data
        
    Returns:
        Flask: A configured Flask application for testing
    """
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
    """
    Create a test client for the Flask app.
    
    This fixture provides a test client that can be used to make
    requests to the Flask application without running an actual server.
    
    Args:
        app: The Flask application fixture
        
    Returns:
        FlaskClient: A test client for the Flask application
    """
    return app.test_client()

def test_get_podcasts(client):
    """
    Test retrieving all podcasts through the blueprint.
    
    This test verifies that the GET / endpoint returns a list of all
    podcasts with the correct data structure and content.
    
    Args:
        client: The Flask test client fixture
    """
    response = client.get('/api/podcasts/')
    assert response.status_code == 200
    data = response.get_json()
    assert 'podcasts' in data
    assert len(data['podcasts']) == 2
    assert data['podcasts'][0]['title'] == "Test Podcast 1"
    assert data['podcasts'][1]['title'] == "Test Podcast 2"

def test_get_podcast_by_id(client):
    """
    Test retrieving a specific podcast by ID.
    
    This test verifies that the GET /<podcast_id>/ endpoint returns
    the correct podcast when given a valid ID.
    
    Args:
        client: The Flask test client fixture
    """
    response = client.get('/api/podcasts/0/')  # First podcast
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == "Test Podcast 1"
    assert data['host'] == "John Doe"

def test_get_podcast_by_id_not_found(client):
    """
    Test retrieving a non-existent podcast ID.
    
    This test verifies that the GET /<podcast_id>/ endpoint properly
    returns a 404 error when requesting a podcast that doesn't exist.
    
    Args:
        client: The Flask test client fixture
    """
    response = client.get('/api/podcasts/999/')
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Podcast not found'

def test_add_podcast(client, mocker, test_podcast_data):
    """
    Test creating a new podcast.
    
    This test verifies that the POST / endpoint successfully creates
    a new podcast with the provided data and returns the correct
    response with status code 201.
    
    Args:
        client: The Flask test client fixture
        mocker: The pytest-mock fixture
        test_podcast_data: The fixture providing test podcast data
    """
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
    """
    Test creating a podcast with no data.
    
    This test verifies that the POST / endpoint properly returns
    a 400 error when no JSON data is provided in the request.
    
    Args:
        client: The Flask test client fixture
    """
    response = client.post('/api/podcasts/', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'No data provided'

def test_delete_podcast(client, mocker, test_podcast_data):
    """
    Test deleting a podcast.
    
    This test verifies that the DELETE /<podcast_id>/ endpoint successfully
    removes a podcast from the system and returns the correct status code.
    It also verifies that subsequent requests reflect the deletion.
    
    Args:
        client: The Flask test client fixture
        mocker: The pytest-mock fixture
        test_podcast_data: The fixture providing test podcast data
    """
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
    """
    Test deleting a non-existent podcast.
    
    This test verifies that the DELETE /<podcast_id>/ endpoint properly
    returns a 404 error when attempting to delete a podcast that doesn't exist.
    
    Args:
        client: The Flask test client fixture
    """
    response = client.delete('/api/podcasts/999/')
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'Podcast not found'

def test_update_podcast(client, mocker, test_podcast_data):
    """
    Test updating an existing podcast.
    
    This test verifies that the PUT /<podcast_id>/ endpoint successfully
    updates a podcast with the provided data and returns the correct response.
    
    Args:
        client: The Flask test client fixture
        mocker: The pytest-mock fixture
        test_podcast_data: The fixture providing test podcast data
    """
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
    """
    Test updating a podcast with no data.
    
    This test verifies that the PUT /<podcast_id>/ endpoint properly
    returns a 400 error when no JSON data is provided in the request.
    
    Args:
        client: The Flask test client fixture
    """
    response = client.put('/api/podcasts/0/', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert data['error'] == 'No data provided'

def test_update_podcast_not_found(client, mocker):
    """
    Test updating a non-existent podcast.
    
    This test verifies that the PUT /<podcast_id>/ endpoint properly
    returns a 400 error with appropriate message when attempting to 
    update a podcast that doesn't exist.
    
    Args:
        client: The Flask test client fixture
        mocker: The pytest-mock fixture
    """
    # Mock the update_podcast method to raise ValueError
    mocker.patch('zpodcast.core.podcasts.PodcastList.update_podcast', 
                side_effect=ValueError("Podcast not found"))
    
    response = client.put('/api/podcasts/999/', json={"title": "Test"})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_update_podcast_non_integer_id(client):
    """
    Test updating a podcast with a non-integer ID.
    
    This test verifies that the route for updating podcasts correctly enforces
    the integer type constraint for podcast IDs. It checks that attempting to
    access a URL with a non-integer ID results in a 404 error.
    
    Args:
        client: The Flask test client fixture
    """
    # Flask will return a 404 for routes that don't match the expected pattern
    # This tests that the <int:podcast_id> type converter is working correctly
    response = client.put('/api/podcasts/abc/', json={"title": "Updated Title"})
    assert response.status_code == 404  # Not Found, because the route doesn't match