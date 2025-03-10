from flask import Flask
from zpodcast.routes import register_podcast_playlist_routes, register_podcast_routes
from zpodcast.podcastjson import PodcastJSON
from zpodcast.podcastlist import PodcastList
from zpodcast.podcastplaylist import PodcastPlaylist

class zPodcastApp:
    def __init__(self):
        self.app = Flask(__name__)
        register_podcast_routes(self.app)
        register_podcast_playlist_routes(self.app)
        self.podcast_list = None
        self.podcast_playlist = None

    def create_app(self,directory : str = None):
        if directory is None:
            self.app.config['directory'] = 'data'
        else:
            self.app.config['directory'] = directory
            
        self.load_data()
#        self.app.before_first_request(self.load_data)
        self.app.teardown_appcontext(self.save_data)
        return self.app

    def load_data(self):
        directory = self.app.config['directory']
        self.podcast_list = PodcastJSON.import_podcast_list(f"{directory}/podcast_list.json")
        self.podcast_playlist = PodcastJSON.import_podcast_playlist(f"{directory}/podcast_playlist.json")
        self.app.config['podcast_list'] = self.podcast_list
        self.app.config['podcast_playlist'] = self.podcast_playlist

    def save_data(self, exception):
        directory = self.app.config['directory']
        PodcastJSON.export_podcast_list(self.app.config['podcast_list'], f'{directory}/podcast_list.json')
        PodcastJSON.export_podcast_playlist(self.app.config['podcast_playlist'], f'{directory}/podcast_playlist.json')

if __name__ == '__main__':
    podcast_app = PzodcastApp()
    app = podcast_app.create_app()
    app.run(debug=True)
