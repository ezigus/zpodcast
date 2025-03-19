from flask import Blueprint, jsonify, request
from zpodcast.core.podcasts import PodcastList
from zpodcast.parsers.json import PodcastJSON

podcasts_bp = Blueprint('podcasts', __name__)

@podcasts_bp.route('/', methods=['GET'])
def get_podcasts():
    """Get all podcasts"""
    podcast_list = PodcastList.get_instance()
    return jsonify(podcast_list.to_dict())

@podcasts_bp.route('/<podcast_id>', methods=['GET'])
def get_podcast(podcast_id):
    """Get a specific podcast by ID"""
    podcast_list = PodcastList.get_instance()
    podcast = podcast_list.get_podcast(podcast_id)
    if not podcast:
        return jsonify({"error": "Podcast not found"}), 404
    return jsonify(podcast.to_dict())

@podcasts_bp.route('/', methods=['POST'])
def add_podcast():
    """Add a new podcast"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    podcast_list = PodcastList.get_instance()
    try:
        podcast = podcast_list.add_podcast(data)
        return jsonify(podcast.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@podcasts_bp.route('/<podcast_id>', methods=['PUT'])
def update_podcast(podcast_id):
    """Update a podcast"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    podcast_list = PodcastList.get_instance()
    try:
        podcast = podcast_list.update_podcast(podcast_id, data)
        return jsonify(podcast.to_dict())
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@podcasts_bp.route('/<podcast_id>', methods=['DELETE'])
def delete_podcast(podcast_id):
    """Delete a podcast"""
    podcast_list = PodcastList.get_instance()
    try:
        podcast_list.delete_podcast(podcast_id)
        return "", 204
    except ValueError as e:
        return jsonify({"error": str(e)}), 404 