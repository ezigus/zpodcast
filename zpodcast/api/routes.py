from flask import jsonify, Flask
from zpodcast.core.podcasts import PodcastList
from zpodcast.core.playlists import PodcastPlaylist

def register_podcast_routes(app: Flask):
    @app.route('/podcasts', methods=['GET'])
    def get_podcasts():
        podcast_list = app.config['podcast_list']
        return jsonify(podcast_list.to_dict())

def register_podcast_playlist_routes(app: Flask):
    @app.route('/playlists', methods=['GET'])
    def get_playlists():
        podcast_playlist = app.config['podcast_playlist']
        return jsonify(podcast_playlist.to_dict())
