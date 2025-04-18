"""
Playlists API Blueprint Module

This module provides REST API endpoints for managing podcast playlists in the
ZPodcast application. It includes routes for creating, updating, deleting,
and retrieving playlists and their episodes.

Routes:
    GET /: List all playlists
    GET /<playlist_id>/: Retrieve a specific playlist by ID
    POST /: Create a new playlist
    PUT /<playlist_id>/: Update an existing playlist
    DELETE /<playlist_id>/: Delete a playlist
    POST /<playlist_id>/episodes/: Add an episode to a playlist
    DELETE /<playlist_id>/episodes/<episode_id>/: Remove an episode from a playlist
"""

from flask import Blueprint, jsonify, request
from flasgger import swag_from
from zpodcast.core.playlists import PodcastPlaylist
from zpodcast.core.playlist import PodcastEpisodeList
from zpodcast.core.episode import PodcastEpisode


playlists_bp = Blueprint("playlists", __name__)


@playlists_bp.route("/", methods=["GET"])
@swag_from({
    'responses': {
        200: {
            'description': 'List of all playlists',
            'schema': {
                'type': 'array',
                'items': {'type': 'object'}
            }
        }
    },
    'summary': 'Retrieve all playlists',
    'tags': ['playlists']
})
def get_playlists():
    """
    Retrieve all playlists.

    Returns:
        Response: A Flask response object containing:
            - A list of all playlists.
    """
    playlist = PodcastPlaylist.get_instance()
    return jsonify(playlist.to_dict())


@playlists_bp.route("/<playlist_id>/", methods=["GET"])
def get_playlist(playlist_id):
    """
    Retrieve a specific playlist by its ID.

    Args:
        playlist_id (str): The unique identifier of the playlist.

    Returns:
        Response: A Flask response object containing:
            - The playlist details if found.
            - An error message if the playlist is not found.
    """
    playlist = PodcastPlaylist.get_instance()
    try:
        # Convert playlist_id to integer
        index = int(playlist_id)
        if index < 0 or index >= len(playlist.playlists):
            return jsonify({"error": "Playlist not found"}), 404

        playlist_data = playlist.playlists[index].to_dict()
        return jsonify(playlist_data)
    except (ValueError, IndexError):
        return jsonify({"error": "Playlist not found"}), 404


@playlists_bp.route("/", methods=["POST"])
def create_playlist():
    """
    Create a new playlist.

    Returns:
        Response: A Flask response object containing:
            - The created playlist details.
            - An error message if the request data is invalid.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    playlist = PodcastPlaylist.get_instance()
    try:
        # Create a new playlist
        new_playlist = PodcastEpisodeList(
            name=data.get("name", "New Playlist"), episodes=[]
        )
        playlist.add_playlist(new_playlist)
        return jsonify(new_playlist.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@playlists_bp.route("/<playlist_id>/", methods=["PUT"])
def update_playlist(playlist_id):
    """
    Update an existing playlist.

    Args:
        playlist_id (str): The unique identifier of the playlist.

    Returns:
        Response: A Flask response object containing:
            - The updated playlist details.
            - An error message if the playlist is not found or the request data is invalid.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    playlist = PodcastPlaylist.get_instance()
    try:
        # Convert playlist_id to integer
        index = int(playlist_id)
        if index < 0 or index >= len(playlist.playlists):
            return jsonify({"error": "Playlist not found"}), 404

        # Update the playlist's name
        if "name" in data:
            playlist.playlists[index].name = data["name"]

        return jsonify(playlist.playlists[index].to_dict())
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@playlists_bp.route("/<playlist_id>/", methods=["DELETE"])
def delete_playlist(playlist_id):
    """
    Delete a playlist by its ID.

    Args:
        playlist_id (str): The unique identifier of the playlist.

    Returns:
        Response: A Flask response object containing:
            - An empty response with a 204 status code if successful.
            - An error message if the playlist is not found.
    """
    playlist = PodcastPlaylist.get_instance()
    try:
        # Convert playlist_id to integer
        index = int(playlist_id)
        if index < 0 or index >= len(playlist.playlists):
            return jsonify({"error": "Playlist not found"}), 404

        # Delete the playlist
        playlist.remove_playlist(index)
        return "", 204
    except ValueError:
        return jsonify({"error": "Playlist not found"}), 404


@playlists_bp.route("/<playlist_id>/episodes/", methods=["POST"])
@swag_from({
    'responses': {
        200: {
            'description': 'Updated playlist with new episode',
            'schema': {'type': 'object'}
        },
        400: {'description': 'Invalid input data'},
        404: {'description': 'Playlist not found'}
    },
    'summary': 'Add an episode to a playlist',
    'tags': ['playlists']
})
def add_episode_to_playlist(playlist_id):
    """
    Add an episode to a specific playlist.

    Args:
        playlist_id (str): The unique identifier of the playlist.

    Returns:
        Response: A Flask response object containing:
            - The updated playlist details.
            - An error message if the playlist is not found or the request data is invalid.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    playlist = PodcastPlaylist.get_instance()
    try:
        # Convert playlist_id to integer
        index = int(playlist_id)
        if index < 0 or index >= len(playlist.playlists):
            return jsonify({"error": "Playlist not found"}), 404

        # Validate and create a new PodcastEpisode using centralized validations
        episode = PodcastEpisode(
            title=data.get("title"),
            audio_url=data.get("audio_url"),
            description=data.get("description"),
            pub_date=data.get("pub_date"),
            duration=data.get("duration"),
            episode_number=data.get("episode_number"),
            image_url=data.get("image_url"),
        )
        playlist.playlists[index].add_podcastepisode(episode)
        return jsonify(playlist.playlists[index].to_dict())
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@playlists_bp.route("/<playlist_id>/episodes/<episode_id>/", methods=["DELETE"])
@swag_from({
    'responses': {
        200: {
            'description': 'Updated playlist after episode removal',
            'schema': {'type': 'object'}
        },
        404: {'description': 'Playlist or episode not found'}
    },
    'summary': 'Remove an episode from a playlist',
    'tags': ['playlists']
})
def remove_episode_from_playlist(playlist_id, episode_id):
    """
    Remove an episode from a specific playlist.

    Args:
        playlist_id (str): The unique identifier of the playlist.
        episode_id (str): The unique identifier of the episode.

    Returns:
        Response: A Flask response object containing:
            - The updated playlist details.
            - An error message if the playlist or episode is not found.
    """
    playlist = PodcastPlaylist.get_instance()
    try:
        # Convert IDs to integers
        playlist_index = int(playlist_id)
        episode_index = int(episode_id)

        if playlist_index < 0 or playlist_index >= len(playlist.playlists):
            return jsonify({"error": "Playlist not found"}), 404

        # Remove episode from the playlist
        playlist.playlists[playlist_index].remove_podcastepisode(episode_index)

        return jsonify(playlist.playlists[playlist_index].to_dict())
    except (ValueError, IndexError):
        return jsonify({"error": "Episode not found"}), 404
