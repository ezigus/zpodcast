from flask import Blueprint, jsonify, request
from zpodcast.core.podcasts import PodcastList
from zpodcast.core.episode import PodcastEpisode

episodes_bp = Blueprint('episodes', __name__)

@episodes_bp.route('/<podcast_id>/', methods=['GET'])
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

@episodes_bp.route('/<podcast_id>/<episode_id>/', methods=['GET'])
def get_episode(podcast_id, episode_id):
    """Get a specific episode"""
    podcast_list = PodcastList.get_instance()
    try:
        podcast = podcast_list.get_podcast(int(podcast_id))
        if not podcast:
            return jsonify({"error": "Podcast not found"}), 404
        
        episode = podcast.get_episode(int(episode_id))
        if not episode:
            return jsonify({"error": "Episode not found"}), 404
        return jsonify(episode.to_dict())
    except ValueError:
        return jsonify({"error": "Podcast not found"}), 404