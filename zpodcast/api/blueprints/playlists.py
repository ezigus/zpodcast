from flask import Blueprint, jsonify, request
from zpodcast.core.playlists import PodcastPlaylist
from zpodcast.parsers.json import PodcastJSON

playlists_bp = Blueprint('playlists', __name__)

@playlists_bp.route('/', methods=['GET'])
def get_playlists():
    """Get all playlists"""
    playlist = PodcastPlaylist.get_instance()
    return jsonify(playlist.to_dict())

@playlists_bp.route('/<playlist_id>', methods=['GET'])
def get_playlist(playlist_id):
    """Get a specific playlist by ID"""
    playlist = PodcastPlaylist.get_instance()
    playlist_data = playlist.get_playlist(playlist_id)
    if not playlist_data:
        return jsonify({"error": "Playlist not found"}), 404
    return jsonify(playlist_data)

@playlists_bp.route('/', methods=['POST'])
def create_playlist():
    """Create a new playlist"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    playlist = PodcastPlaylist.get_instance()
    try:
        new_playlist = playlist.create_playlist(data)
        return jsonify(new_playlist), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@playlists_bp.route('/<playlist_id>', methods=['PUT'])
def update_playlist(playlist_id):
    """Update a playlist"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    playlist = PodcastPlaylist.get_instance()
    try:
        updated_playlist = playlist.update_playlist(playlist_id, data)
        return jsonify(updated_playlist)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@playlists_bp.route('/<playlist_id>', methods=['DELETE'])
def delete_playlist(playlist_id):
    """Delete a playlist"""
    playlist = PodcastPlaylist.get_instance()
    try:
        playlist.delete_playlist(playlist_id)
        return "", 204
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@playlists_bp.route('/<playlist_id>/episodes', methods=['POST'])
def add_episode_to_playlist(playlist_id):
    """Add an episode to a playlist"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    playlist = PodcastPlaylist.get_instance()
    try:
        updated_playlist = playlist.add_episode(playlist_id, data)
        return jsonify(updated_playlist)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@playlists_bp.route('/<playlist_id>/episodes/<episode_id>', methods=['DELETE'])
def remove_episode_from_playlist(playlist_id, episode_id):
    """Remove an episode from a playlist"""
    playlist = PodcastPlaylist.get_instance()
    try:
        updated_playlist = playlist.remove_episode(playlist_id, episode_id)
        return jsonify(updated_playlist)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404 