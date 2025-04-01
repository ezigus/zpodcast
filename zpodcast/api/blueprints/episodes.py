"""
Episodes API Blueprint Module

This module provides REST API endpoints for managing podcast episodes in the
ZPodcast application. It includes routes for listing and retrieving episodes
for specific podcasts.

Routes:
    GET /<podcast_id>/: List all episodes for a specific podcast
    GET /<podcast_id>/<episode_id>/: Retrieve a specific episode by ID
"""

from flask import Blueprint, jsonify
from zpodcast.core.podcasts import PodcastList


episodes_bp = Blueprint("episodes", __name__)


@episodes_bp.route("/<podcast_id>/", methods=["GET"])
def get_episodes(podcast_id):
    """
    Retrieve all episodes for a specific podcast.

    Args:
        podcast_id (str): The unique identifier of the podcast.

    Returns:
        Response: A Flask response object containing:
            - A list of episodes if the podcast is found.
            - An error message if the podcast is not found.
    """
    podcast_list = PodcastList.get_instance()
    try:
        podcast = podcast_list.get_podcast(int(podcast_id))
        if not podcast:
            return jsonify({"error": "Podcast not found"}), 404
        return jsonify(podcast.get_episodes())
    except ValueError:
        return jsonify({"error": "Podcast not found"}), 404


@episodes_bp.route("/<podcast_id>/<episode_id>/", methods=["GET"])
def get_episode(podcast_id, episode_id):
    """
    Retrieve a specific episode by its ID.

    Args:
        podcast_id (str): The unique identifier of the podcast.
        episode_id (str): The unique identifier of the episode.

    Returns:
        Response: A Flask response object containing:
            - The episode details if found.
            - An error message if the episode or podcast is not found.
    """
    podcast_list = PodcastList.get_instance()

    # First try to parse the podcast_id
    try:
        podcast_id_int = int(podcast_id)
    except ValueError:
        return jsonify({"error": "Podcast not found"}), 404

    # Get the podcast, handle both ValueError (invalid index) and None (not found)
    try:
        podcast = podcast_list.get_podcast(podcast_id_int)
        if not podcast:
            return jsonify({"error": "Podcast not found"}), 404
    except ValueError:
        return jsonify({"error": "Podcast not found"}), 404

    # Now try to parse the episode_id
    try:
        episode_id_int = int(episode_id)
    except ValueError:
        return jsonify({"error": "Episode not found"}), 404

    # Get the episode
    # Use PodcastEpisode's centralized validations
    try:
        episode = podcast.get_episode(episode_id_int)
        if not episode:
            return jsonify({"error": "Episode not found"}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify(episode.to_dict())
