from flask import Flask
from zpodcast.routes import register_podcast_playlist_routes, register_podcast_routes
from zpodcast.podcastjson import PodcastJSON
from zpodcast.podcastlist import PodcastList
from zpodcast.podcastplaylist import PodcastPlaylist

class PodcastApp:
    def __init__(self):
        self.app = Flask(__name__)
        register_podcast_routes(self.app)
        register_podcast_playlist_routes(self.app)
        self.podcast_list = None
        self.podcast_playlist = None

    def create_app(self):
        self.load_data()
        self.app.before_first_request(self.load_data)
        self.app.teardown_appcontext(self.save_data)
        return self.app

    def load_data(self):
        self.podcast_list = PodcastJSON.import_podcast_list('data/podcast_list.json')
        self.podcast_playlist = PodcastJSON.import_podcast_playlist('data/podcast_playlist.json')
        self.app.config['podcast_list'] = self.podcast_list
        self.app.config['podcast_playlist'] = self.podcast_playlist

    def save_data(self, exception):
        PodcastJSON.export_podcast_list(self.app.config['podcast_list'], 'data/podcast_list.json')
        PodcastJSON.export_podcast_playlist(self.app.config['podcast_playlist'], 'data/podcast_playlist.json')

if __name__ == '__main__':
    podcast_app = PodcastApp()
    app = podcast_app.create_app()
    app.run(debug=True)
