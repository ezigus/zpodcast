"""
Swagger Documentation Testing Module

This module contains tests that verify the API's Swagger documentation
is correctly configured and matches the actual implementation.
"""
import pytest
from zpodcast.api.app import zPodcastApp
import json
import os


@pytest.fixture
def app():
    """Create a test Flask app instance with Swagger enabled"""
    app_instance = zPodcastApp()
    # Use test data directory
    test_data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    return app_instance.create_app(test_data_dir)


@pytest.fixture
def client(app):
    """Create a test client for the Flask app"""
    return app.test_client()


def test_swagger_json_accessible(client):
    """Test that the Swagger JSON specification is accessible"""
    response = client.get('/apispec_1.json')
    assert response.status_code == 200
    swagger_json = json.loads(response.data)
    
    # Basic structure checks
    assert 'info' in swagger_json
    assert 'title' in swagger_json['info']
    assert swagger_json['info']['title'] == 'ZPodcast API'
    assert 'paths' in swagger_json


def test_podcasts_endpoints_in_swagger(client):
    """Test that all podcast endpoints are documented in Swagger"""
    response = client.get('/apispec_1.json')
    assert response.status_code == 200
    swagger_json = json.loads(response.data)
    
    # Check that all podcast endpoints are documented
    assert '/api/podcasts/' in swagger_json['paths']
    assert 'get' in swagger_json['paths']['/api/podcasts/']
    assert 'post' in swagger_json['paths']['/api/podcasts/']
    
    # Ensure podcast ID parameter endpoint exists
    podcast_id_path = '/api/podcasts/{podcast_id}/'
    assert podcast_id_path in swagger_json['paths']
    assert 'get' in swagger_json['paths'][podcast_id_path]
    assert 'put' in swagger_json['paths'][podcast_id_path]
    assert 'delete' in swagger_json['paths'][podcast_id_path]


def test_podcast_schema_in_parameters(client):
    """Test that the podcast schema is correctly defined in Swagger parameters"""
    response = client.get('/apispec_1.json')
    assert response.status_code == 200
    swagger_json = json.loads(response.data)
    
    # In Flasgger, schemas are defined inline within parameters for POST/PUT requests
    post_path = swagger_json['paths']['/api/podcasts/']['post']
    
    # Find the body parameter which contains our schema
    body_param = None
    for param in post_path['parameters']:
        if param.get('in') == 'body':
            body_param = param
            break
    
    # Ensure we found a body parameter
    assert body_param is not None, "No body parameter found for POST /api/podcasts/"
    
    # Check that the schema contains expected properties
    schema = body_param['schema']
    assert 'properties' in schema
    properties = schema['properties']
    
    # Verify required properties exist
    assert 'title' in properties
    assert 'podcast_url' in properties
    assert 'description' in properties
    assert 'host' in properties
    assert 'podcast_priority' in properties
    
    # Verify required fields are listed
    assert 'required' in schema
    assert 'title' in schema['required']
    assert 'podcast_url' in schema['required']


def test_swagger_response_codes(client):
    """Test that Swagger documentation includes appropriate response codes"""
    response = client.get('/apispec_1.json')
    assert response.status_code == 200
    swagger_json = json.loads(response.data)
    
    # Check GET podcast endpoint
    get_podcast_path = '/api/podcasts/{podcast_id}/'
    get_podcast = swagger_json['paths'][get_podcast_path]['get']
    responses = get_podcast['responses']
    
    # Check status codes
    assert '200' in responses
    assert '404' in responses
    
    # Check POST endpoint for creation status code
    post_podcast_path = '/api/podcasts/'
    post_podcast = swagger_json['paths'][post_podcast_path]['post']
    responses = post_podcast['responses']
    assert '201' in responses
    assert '400' in responses
    assert '500' in responses


def test_swagger_implementation_consistency(client):
    """Test that the implementation matches what is documented in Swagger"""
    # This test requires more advanced setup to introspect Flask routes
    
    # First get the Swagger JSON
    response = client.get('/apispec_1.json')
    assert response.status_code == 200
    swagger_json = json.loads(response.data)
    
    # Get all podcast paths from Swagger docs
    swagger_paths = set(swagger_json['paths'].keys())
    
    # Verify core podcast endpoints are documented
    expected_paths = {
        '/api/podcasts/',
        '/api/podcasts/{podcast_id}/'
    }
    
    # Check if all expected paths are in Swagger
    for path in expected_paths:
        assert path in swagger_paths, f"Path {path} missing from Swagger docs"
    
    # Verify that the method handlers match
    # For the list endpoint
    list_endpoint = swagger_json['paths']['/api/podcasts/']
    assert 'get' in list_endpoint, "GET method missing for /api/podcasts/"
    assert 'post' in list_endpoint, "POST method missing for /api/podcasts/"
    
    # For the detail endpoint
    detail_endpoint = swagger_json['paths']['/api/podcasts/{podcast_id}/']
    assert 'get' in detail_endpoint, "GET method missing for /api/podcasts/{podcast_id}/"
    assert 'put' in detail_endpoint, "PUT method missing for /api/podcasts/{podcast_id}/"
    assert 'delete' in detail_endpoint, "DELETE method missing for /api/podcasts/{podcast_id}/"