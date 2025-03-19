from flask import Flask, jsonify
from zpodcast.api.routes import register_podcast_playlist_routes, register_podcast_routes
from zpodcast.parsers.json import PodcastJSON
from zpodcast.core.podcasts import PodcastList
from zpodcast.core.playlists import PodcastPlaylist
import os

class zPodcastApp:
    def __init__(self):
        self.app = Flask(__name__)
        register_podcast_routes(self.app)
        register_podcast_playlist_routes(self.app)

    def create_app(self, data_dir):
        self.app.config['DATA_DIR'] = data_dir

        # Load podcast_list
        podcast_list_path = os.path.join(data_dir, 'podcast_list.json')
        self.app.config['podcast_list'] = PodcastJSON.import_podcast_list(podcast_list_path)

        # Load podcast_playlist
        podcast_playlist_path = os.path.join(data_dir, 'podcast_playlist.json')
        self.app.config['podcast_playlist'] = PodcastJSON.import_podcast_playlist(podcast_playlist_path)

        return self.app

app = Flask(__name__)
register_podcast_routes(app)
register_podcast_playlist_routes(app)

@app.route('/')
def index():
    return jsonify({"message": "Welcome to ZPodcast API"})

if __name__ == '__main__':
    app.run(debug=True)
