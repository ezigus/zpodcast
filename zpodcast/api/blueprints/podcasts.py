"""
Podcasts API Blueprint Module

This module provides REST API endpoints for managing podcasts in the
ZPodcast application. It includes routes for listing, retrieving, creating,
updating, and deleting podcasts.

Routes:
    GET /: List all podcasts
    GET /<int:podcast_id>/: Retrieve a specific podcast by ID
    POST /: Create a new podcast
    PUT /<int:podcast_id>/: Update an existing podcast
    DELETE /<int:podcast_id>/: Delete a podcast
"""

from typing import Dict, Tuple, Any, Optional

from flask import Blueprint, jsonify, request, Response
import validators

from zpodcast.core.podcasts import PodcastList
from zpodcast.core.podcast import PodcastData

# Define Swagger schemas for podcast objects
PodcastSchema = {
    "type": "object",
    "properties": {
        "id": {"type": "integer", "description": "Unique podcast identifier"},
        "title": {"type": "string", "description": "Podcast title"},
        "podcast_url": {"type": "string", "description": "RSS feed URL"},
        "host": {"type": "string", "description": "Podcast host/author"},
        "description": {"type": "string", "description": "Podcast description"},
        "episodelists": {
            "type": "array",
            "items": {"type": "object"},
            "description": "Lists of episodes for this podcast",
        },
        "podcast_priority": {"type": "integer", "description": "User priority (0-10)"},
        "image_url": {"type": "string", "description": "Podcast cover art URL"},
    },
    "required": ["title", "podcast_url"],
}

PodcastListSchema = {
    "type": "object",
    "properties": {"podcasts": {"type": "array", "items": PodcastSchema}},
}

# Constants for validation
MAX_TITLE_LENGTH = 200
MAX_DESCRIPTION_LENGTH = 5000
MAX_PRIORITY = 10
MIN_PRIORITY = 0

podcasts_bp = Blueprint("podcasts", __name__)


def validate_podcast_data(
    data: Dict[str, Any], required_fields: bool = True
) -> Optional[str]:
    """
    Validate podcast data against requirements.

    This function checks if the provided podcast data meets all validation
    requirements such as having required fields, valid URLs, proper format, etc.

    Args:
        data (Dict[str, Any]): The podcast data to validate
        required_fields (bool): Whether to enforce required fields validation
                              Set to False for partial updates (PUT requests)

    Returns:
        Optional[str]: Error message if validation fails, None if validation passes

    Example:
        >>> error = validate_podcast_data({"title": "My Podcast"})
        >>> if error:
        >>>     print(f"Validation error: {error}")
    """
    # Check required fields for POST requests
    if required_fields:
        if not data.get("title"):
            return "Title is required"
        if not data.get("podcast_url"):
            return "Podcast URL is required"

    # Validate title if present
    if "title" in data and data["title"]:
        if not isinstance(data["title"], str):
            return "Title must be a string"
        if len(data["title"]) > MAX_TITLE_LENGTH:
            return f"Title exceeds maximum length of {MAX_TITLE_LENGTH} characters"

    # Validate podcast URL if present
    if "podcast_url" in data and data["podcast_url"]:
        if not isinstance(data["podcast_url"], str):
            return "Podcast URL must be a string"
        if not validators.url(data["podcast_url"]):
            return "Invalid podcast URL format"

    # Validate description if present
    if "description" in data and data["description"]:
        if not isinstance(data["description"], str):
            return "Description must be a string"
        if len(data["description"]) > MAX_DESCRIPTION_LENGTH:
            return (
                f"Description exceeds maximum length of {MAX_DESCRIPTION_LENGTH} "
                f"characters"
            )

    # Validate podcast priority if present
    if "podcast_priority" in data and data["podcast_priority"] is not None:
        try:
            priority = int(data["podcast_priority"])
            if priority < MIN_PRIORITY or priority > MAX_PRIORITY:
                return (
                    f"Podcast priority must be between {MIN_PRIORITY} and "
                    f"{MAX_PRIORITY}"
                )
        except (ValueError, TypeError):
            return "Podcast priority must be an integer"

    # Validate image URL if present
    if "image_url" in data and data["image_url"]:
        if not isinstance(data["image_url"], str):
            return "Image URL must be a string"
        if not validators.url(data["image_url"]):
            return "Invalid image URL format"

    return None


@podcasts_bp.route("/", methods=["GET"])
def get_podcasts() -> Response:
    """
    Retrieve a list of all podcasts.

    Returns:
        Response: A Flask response object containing:
            - A list of all podcasts with their metadata.
    """
    podcast_list = PodcastList.get_instance()
    return jsonify(podcast_list.to_dict())


@podcasts_bp.route("/<int:podcast_id>/", methods=["GET"])
def get_podcast(podcast_id: int) -> Tuple[Response, int]:
    """
    Retrieve a specific podcast by its ID.

    Args:
        podcast_id (int): The unique identifier of the podcast.

    Returns:
        Tuple[Response, int]: A tuple containing:
            - The podcast details if found.
            - An error message if the podcast is not found.
    """
    podcast_list = PodcastList.get_instance()
    try:
        podcast = podcast_list.get_podcast(podcast_id)
        return jsonify(podcast.to_dict()), 200
    except ValueError:
        return jsonify({"error": "Podcast not found"}), 404


@podcasts_bp.route("/", methods=["POST"])
def add_podcast() -> Tuple[Response, int]:
    """
    Create a new podcast.

    Returns:
        Tuple[Response, int]: A tuple containing:
            - The created podcast details.
            - An error message if the request data is invalid.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Validate podcast data
    validation_error = validate_podcast_data(data)
    if validation_error:
        return jsonify({"error": validation_error}), 400

    podcast_list = PodcastList.get_instance()
    try:
        podcast = PodcastData(**data)  # Ensure PodcastData object is created
        podcast_list.add_podcast(podcast)
        return jsonify(podcast.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@podcasts_bp.route("/<int:podcast_id>/", methods=["PUT"])
def update_podcast(podcast_id: int) -> Tuple[Response, int]:
    """
    Update an existing podcast.

    Args:
        podcast_id (int): The unique identifier of the podcast.

    Returns:
        Tuple[Response, int]: A tuple containing:
            - The updated podcast details.
            - An error message if the podcast is not found or the request data is invalid.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Validate podcast data (not requiring all fields for updates)
    validation_error = validate_podcast_data(data, required_fields=False)
    if validation_error:
        return jsonify({"error": validation_error}), 400

    podcast_list = PodcastList.get_instance()
    try:
        podcast = podcast_list.update_podcast(podcast_id, data)
        return jsonify(podcast.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@podcasts_bp.route("/<int:podcast_id>/", methods=["DELETE"])
def delete_podcast(podcast_id: int) -> Tuple[str, int]:
    """
    Delete a podcast by its ID.

    Args:
        podcast_id (int): The unique identifier of the podcast.

    Returns:
        Tuple[str, int]: A tuple containing:
            - An empty response with a 204 status code if successful.
            - An error message if the podcast is not found.
    """
    podcast_list = PodcastList.get_instance()
    try:
        podcast_list.delete_podcast(podcast_id)
        return "", 204
    except ValueError:
        return jsonify({"error": "Podcast not found"}), 404
