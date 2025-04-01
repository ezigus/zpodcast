from flask import Blueprint, jsonify
from zpodcast.core.podcasts import PodcastList


episodes_bp = Blueprint("episodes", __name__)


@episodes_bp.route("/<podcast_id>/", methods=["GET"])
def get_episodes(podcast_id):
    """Get all episodes for a podcast"""
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
    """Get a specific episode"""
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
    episode = podcast.get_episode(episode_id_int)
    if not episode:
        return jsonify({"error": "Episode not found"}), 404

    return jsonify(episode.to_dict())
