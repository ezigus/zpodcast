from flask import Blueprint, jsonify, request
from zpodcast.core.podcasts import PodcastList
from zpodcast.core.episode import Episode

episodes_bp = Blueprint('episodes', __name__)

@episodes_bp.route('/<podcast_id>', methods=['GET'])
def get_episodes(podcast_id):
    """Get all episodes for a podcast"""
    podcast_list = PodcastList.get_instance()
    podcast = podcast_list.get_podcast(podcast_id)
    if not podcast:
        return jsonify({"error": "Podcast not found"}), 404
    return jsonify(podcast.get_episodes())

@episodes_bp.route('/<podcast_id>/<episode_id>', methods=['GET'])
def get_episode(podcast_id, episode_id):
    """Get a specific episode"""
    podcast_list = PodcastList.get_instance()
    podcast = podcast_list.get_podcast(podcast_id)
    if not podcast:
        return jsonify({"error": "Podcast not found"}), 404
    
    episode = podcast.get_episode(episode_id)
    if not episode:
        return jsonify({"error": "Episode not found"}), 404
    return jsonify(episode.to_dict())

@episodes_bp.route('/<podcast_id>/<episode_id>/download', methods=['POST'])
def download_episode(podcast_id, episode_id):
    """Download an episode"""
    podcast_list = PodcastList.get_instance()
    podcast = podcast_list.get_podcast(podcast_id)
    if not podcast:
        return jsonify({"error": "Podcast not found"}), 404
    
    episode = podcast.get_episode(episode_id)
    if not episode:
        return jsonify({"error": "Episode not found"}), 404
    
    try:
        episode.download()
        return jsonify({"message": "Download started"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@episodes_bp.route('/<podcast_id>/<episode_id>/progress', methods=['GET'])
def get_episode_progress(podcast_id, episode_id):
    """Get download progress for an episode"""
    podcast_list = PodcastList.get_instance()
    podcast = podcast_list.get_podcast(podcast_id)
    if not podcast:
        return jsonify({"error": "Podcast not found"}), 404
    
    episode = podcast.get_episode(episode_id)
    if not episode:
        return jsonify({"error": "Episode not found"}), 404
    
    return jsonify({
        "progress": episode.get_download_progress(),
        "status": episode.get_download_status()
    }) 