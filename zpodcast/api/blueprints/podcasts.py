"""
Podcast API Blueprint Module

This module provides REST API endpoints for managing podcasts in the ZPodcast application.
It includes routes for listing, retrieving, creating, updating, and deleting podcasts.

The blueprint follows RESTful design principles with appropriate HTTP methods
for each operation and consistent URL patterns.

Routes:
    GET /: List all podcasts
    GET /<int:podcast_id>/: Get a specific podcast by ID
    POST /: Create a new podcast
    PUT /<int:podcast_id>/: Update an existing podcast
    DELETE /<int:podcast_id>/: Delete a podcast
"""
from typing import Dict, List, Tuple, Union, Any
from flask import Blueprint, jsonify, request, Response
from flasgger import swag_from
from zpodcast.core.podcasts import PodcastList
from zpodcast.parsers.json import PodcastJSON
from zpodcast.core.podcast import PodcastData

# Define Swagger schemas for podcast objects
PodcastSchema = {
    'type': 'object',
    'properties': {
        'id': {'type': 'integer', 'description': 'Unique podcast identifier'},
        'title': {'type': 'string', 'description': 'Podcast title'},
        'podcast_url': {'type': 'string', 'description': 'RSS feed URL'},
        'host': {'type': 'string', 'description': 'Podcast host/author'},
        'description': {'type': 'string', 'description': 'Podcast description'},
        'episodelists': {
            'type': 'array', 
            'items': {'type': 'object'},
            'description': 'Lists of episodes for this podcast'
        },
        'podcast_priority': {'type': 'integer', 'description': 'User priority (0-10)'},
        'image_url': {'type': 'string', 'description': 'Podcast cover art URL'}
    },
    'required': ['title', 'podcast_url']
}

PodcastListSchema = {
    'type': 'object',
    'properties': {
        'podcasts': {
            'type': 'array',
            'items': PodcastSchema
        }
    }
}

podcasts_bp = Blueprint('podcasts', __name__)

@podcasts_bp.route('/', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'List of all podcasts',
            'schema': PodcastListSchema
        },
        500: {
            'description': 'Server error'
        }
    },
    'summary': 'Retrieves all podcasts',
    'tags': ['podcasts']
})
def get_podcasts() -> Response:
    """
    Retrieve a list of all podcasts.
    
    This endpoint returns all podcasts stored in the system with their
    metadata. It does not include the full episode lists to keep the 
    response size manageable.
    
    Returns:
        Response: A Flask response object with JSON containing:
            - podcasts (List[Dict]): A list of podcast objects with their metadata
    
    Example:
        >>> response = requests.get('/api/podcasts/')
        >>> podcasts = response.json()['podcasts']
    """
    podcast_list = PodcastList.get_instance()
    return jsonify(podcast_list.to_dict())

@podcasts_bp.route('/<int:podcast_id>/', methods=['GET'])
@swag_from({
    'parameters': [
        {
            'name': 'podcast_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'Unique identifier of the podcast'
        }
    ],
    'responses': {
        200: {
            'description': 'Podcast details',
            'schema': PodcastSchema
        },
        404: {
            'description': 'Podcast not found'
        }
    },
    'summary': 'Get podcast by ID',
    'tags': ['podcasts']
})
def get_podcast(podcast_id: int) -> Tuple[Response, int]:
    """
    Retrieve a specific podcast by its ID.
    
    This endpoint returns detailed information about a single podcast,
    identified by its unique ID.
    
    Args:
        podcast_id (int): The unique identifier of the podcast to retrieve
    
    Returns:
        Tuple[Response, int]: A tuple containing:
            - A Flask response object with JSON containing the podcast data
            - HTTP status code (200 for success, 404 for not found)
    
    Raises:
        ValueError: If the podcast with the given ID does not exist
              (handled internally, returns 404 response)
    
    Example:
        >>> response = requests.get('/api/podcasts/42/')
        >>> podcast = response.json()
        >>> print(podcast['title'])
    """
    podcast_list = PodcastList.get_instance()
    try:
        podcast = podcast_list.get_podcast(podcast_id)
        return jsonify(podcast.to_dict()), 200
    except ValueError:
        return jsonify({"error": "Podcast not found"}), 404

@podcasts_bp.route('/', methods=['POST'])
@swag_from({
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'schema': PodcastSchema,
            'required': True,
            'description': 'Podcast data to create'
        }
    ],
    'responses': {
        201: {
            'description': 'Podcast created successfully',
            'schema': PodcastSchema
        },
        400: {
            'description': 'Invalid input data'
        },
        500: {
            'description': 'Server error'
        }
    },
    'summary': 'Create a new podcast',
    'tags': ['podcasts']
})
def add_podcast() -> Tuple[Response, int]:
    """
    Create a new podcast.
    
    This endpoint creates a new podcast from the provided JSON data.
    The request must include all required fields for a podcast.
    
    Required fields in request body:
        - title: The title of the podcast
        - podcast_url: The URL of the podcast's RSS feed
    
    Optional fields:
        - host: The name of the podcast's host/author
        - description: A description of the podcast
        - podcast_priority: User-defined priority ranking (0-10)
        - image_url: URL to the podcast's cover art
    
    Returns:
        Tuple[Response, int]: A tuple containing:
            - A Flask response object with JSON of the created podcast
            - HTTP status code (201 for created, 400 for bad request)
    
    Raises:
        ValueError: If the podcast data is invalid or missing required fields
              (handled internally, returns 400 response)
    
    Example:
        >>> data = {
        >>>     "title": "Example Podcast",
        >>>     "podcast_url": "https://example.com/feed.xml",
        >>>     "host": "Jane Doe",
        >>>     "description": "An example podcast"
        >>> }
        >>> response = requests.post('/api/podcasts/', json=data)
        >>> new_podcast = response.json()
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    podcast_list = PodcastList.get_instance()
    try:
        podcast = PodcastData(**data)  # Ensure PodcastData object is created
        podcast_list.add_podcast(podcast)
        return jsonify(podcast.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@podcasts_bp.route('/<int:podcast_id>/', methods=['PUT'])
@swag_from({
    'parameters': [
        {
            'name': 'podcast_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'Unique identifier of the podcast to update'
        },
        {
            'name': 'body',
            'in': 'body',
            'schema': PodcastSchema,
            'required': True,
            'description': 'Updated podcast data'
        }
    ],
    'responses': {
        200: {
            'description': 'Podcast updated successfully',
            'schema': PodcastSchema
        },
        400: {
            'description': 'Invalid input data or podcast not found'
        },
        500: {
            'description': 'Server error'
        }
    },
    'summary': 'Update an existing podcast',
    'tags': ['podcasts']
})
def update_podcast(podcast_id: int) -> Tuple[Response, int]:
    """
    Update an existing podcast.
    
    This endpoint updates a podcast identified by its ID with the 
    provided JSON data. Only the fields included in the request will be updated.
    
    Args:
        podcast_id (int): The unique identifier of the podcast to update
    
    Returns:
        Tuple[Response, int]: A tuple containing:
            - A Flask response object with JSON of the updated podcast
            - HTTP status code (200 for success, 400 for bad request)
    
    Raises:
        ValueError: If the podcast with the given ID does not exist
              or if the update data is invalid
              (handled internally, returns 400 response)
    
    Example:
        >>> update_data = {
        >>>     "title": "Updated Title",
        >>>     "description": "New description"
        >>> }
        >>> response = requests.put('/api/podcasts/42/', json=update_data)
        >>> updated_podcast = response.json()
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    podcast_list = PodcastList.get_instance()
    try:
        podcast = podcast_list.update_podcast(podcast_id, data)
        return jsonify(podcast.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@podcasts_bp.route('/<int:podcast_id>/', methods=['DELETE'])
@swag_from({
    'parameters': [
        {
            'name': 'podcast_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'Unique identifier of the podcast to delete'
        }
    ],
    'responses': {
        204: {
            'description': 'Podcast deleted successfully'
        },
        404: {
            'description': 'Podcast not found'
        },
        500: {
            'description': 'Server error'
        }
    },
    'summary': 'Delete a podcast',
    'tags': ['podcasts']
})
def delete_podcast(podcast_id: int) -> Tuple[str, int]:
    """
    Delete a podcast.
    
    This endpoint removes a podcast identified by its ID from the system.
    
    Args:
        podcast_id (int): The unique identifier of the podcast to delete
    
    Returns:
        Tuple[str, int]: A tuple containing:
            - An empty string for successful deletion
            - HTTP status code (204 for no content, 404 for not found)
    
    Raises:
        ValueError: If the podcast with the given ID does not exist
              (handled internally, returns 404 response)
    
    Example:
        >>> response = requests.delete('/api/podcasts/42/')
        >>> assert response.status_code == 204
    """
    podcast_list = PodcastList.get_instance()
    try:
        podcast_list.delete_podcast(podcast_id)
        return "", 204
    except ValueError:
        return jsonify({"error": "Podcast not found"}), 404