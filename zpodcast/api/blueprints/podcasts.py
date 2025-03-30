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
from zpodcast.core.podcasts import PodcastList
from zpodcast.parsers.json import PodcastJSON
from zpodcast.core.podcast import PodcastData

podcasts_bp = Blueprint('podcasts', __name__)

@podcasts_bp.route('/', methods=['GET'])
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