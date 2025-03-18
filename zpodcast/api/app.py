from flask import Flask, jsonify
from zpodcast.api.routes import register_podcast_playlist_routes, register_podcast_routes
from zpodcast.parsers.json import PodcastJSON
from zpodcast.core.podcasts import PodcastList
from zpodcast.core.playlists import PodcastPlaylist

class zPodcastApp:
    def __init__(self):
        self.app = Flask(__name__)
        register_podcast_routes(self.app)
        register_podcast_playlist_routes(self.app)

    def create_app(self, data_dir):
        self.app.config['DATA_DIR'] = data_dir
        return self.app

app = Flask(__name__)
register_podcast_routes(app)
register_podcast_playlist_routes(app)

# Load podcast list and playlist from JSON files
data_dir = 'data/'  # Adjust the path if necessary
podcast_list_path = f"{data_dir}podcast_list.json"
podcast_playlist_path = f"{data_dir}podcast_playlist.json"

try:
    podcast_list = PodcastJSON.import_podcast_list(podcast_list_path)
    podcast_playlist = PodcastJSON.import_podcast_playlist(podcast_playlist_path)
except FileNotFoundError as e:
    print(f"Error loading data: {e}")
    podcast_list = PodcastList([])
    podcast_playlist = PodcastPlaylist(name="Default Playlist", episodes=[])

# Set the configurations
app.config['podcast_list'] = podcast_list
app.config['podcast_playlist'] = podcast_playlist

@app.route('/')
def index():
    return jsonify({"message": "Welcome to ZPodcast API"})

if __name__ == '__main__':
    app.run(debug=True)
