from flask import jsonify
from zpodcast.podcastjson import PodcastJSON
from zpodcast.podcastlist import PodcastList
from zpodcast.podcastplaylist import PodcastPlaylist

def register_routes(app):
    @app.route('/podcasts', methods=['GET'])
    def get_podcasts():
        podcast_list = PodcastJSON.import_podcast_list('test_podcast_list.json')
        return jsonify(podcast_list.to_dict())

    @app.route('/playlists', methods=['GET'])
    def get_playlists():
        podcast_playlist = PodcastJSON.import_podcast_playlist('test_podcast_list.json')
        return jsonify(podcast_playlist.to_dict())
