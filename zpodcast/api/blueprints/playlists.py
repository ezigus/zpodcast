from flask import Blueprint, jsonify, request
from zpodcast.core.playlists import PodcastPlaylist
from zpodcast.core.playlist import PodcastEpisodeList
from zpodcast.core.episode import PodcastEpisode


playlists_bp = Blueprint("playlists", __name__)


@playlists_bp.route("/", methods=["GET"])
def get_playlists():
    """Get all playlists"""
    playlist = PodcastPlaylist.get_instance()
    return jsonify(playlist.to_dict())


@playlists_bp.route("/<playlist_id>/", methods=["GET"])
def get_playlist(playlist_id):
    """Get a specific playlist by ID"""
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
    """Create a new playlist"""
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
    """Update a playlist"""
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
    """Delete a playlist"""
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
def add_episode_to_playlist(playlist_id):
    """Add an episode to a playlist"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    playlist = PodcastPlaylist.get_instance()
    try:
        # Convert playlist_id to integer
        index = int(playlist_id)
        if index < 0 or index >= len(playlist.playlists):
            return jsonify({"error": "Playlist not found"}), 404

        # Add episode to the playlist
        episode = PodcastEpisode(**data)
        playlist.playlists[index].add_podcastepisode(episode)

        return jsonify(playlist.playlists[index].to_dict())
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@playlists_bp.route("/<playlist_id>/episodes/<episode_id>/", methods=["DELETE"])
def remove_episode_from_playlist(playlist_id, episode_id):
    """Remove an episode from a playlist"""
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
