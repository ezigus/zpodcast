from flask import Flask, jsonify
from flasgger import Swagger
from zpodcast.api.blueprints import podcasts_bp, playlists_bp, episodes_bp
from zpodcast.parsers.json import PodcastJSON
from zpodcast.core.podcasts import PodcastList
from zpodcast.core.playlists import PodcastPlaylist
import os

# Define Swagger template
swagger_template = {
    'info': {
        'title': 'ZPodcast API',
        'description': 'API for managing podcasts and playlists',
        'version': '1.0.0',
        'contact': {
            'name': 'ZPodcast Team',
            'email': 'support@zpodcast.example.com'
        }
    },
    'tags': [
        {
            'name': 'podcasts',
            'description': 'Podcast management operations'
        },
        {
            'name': 'playlists',
            'description': 'Playlist management operations'
        },
        {
            'name': 'episodes',
            'description': 'Episode management operations'
        }
    ]
}

class zPodcastApp:
    def __init__(self):
        self.app = Flask(__name__)
        self._register_blueprints()
        self._setup_error_handlers()

    def _register_blueprints(self):
        """Register all blueprints with their respective URL prefixes"""
        self.app.register_blueprint(podcasts_bp, url_prefix='/api/podcasts')
        self.app.register_blueprint(playlists_bp, url_prefix='/api/playlists')
        self.app.register_blueprint(episodes_bp, url_prefix='/api/episodes')

    def _setup_error_handlers(self):
        """Setup error handlers for common HTTP errors"""
        @self.app.errorhandler(404)
        def not_found_error(error):
            return jsonify({"error": "Resource not found"}), 404

        @self.app.errorhandler(400)
        def bad_request_error(error):
            return jsonify({"error": "Bad request"}), 400

        @self.app.errorhandler(500)
        def internal_server_error(error):
            return jsonify({"error": "Internal server error"}), 500

    def create_app(self, data_dir):
        """Create and configure the Flask application"""
        self.app.config['DATA_DIR'] = data_dir

        # Load podcast_list
        podcast_list_path = os.path.join(data_dir, 'podcast_list.json')
        self.app.config['podcast_list'] = PodcastJSON.import_podcast_list(podcast_list_path)

        # Load podcast_playlist
        podcast_playlist_path = os.path.join(data_dir, 'podcast_playlist.json')
        self.app.config['podcast_playlist'] = PodcastJSON.import_podcast_playlist(podcast_playlist_path)
        
        # Initialize Swagger documentation
        Swagger(self.app, template=swagger_template)

        return self.app

    @staticmethod
    def create_app_factory(data_dir):
        """Factory function to create the application"""
        app = zPodcastApp()
        return app.create_app(data_dir)

# Create the application instance
app = zPodcastApp().create_app(os.getenv('ZPODCAST_DATA_DIR', 'data'))

@app.route('/')
def index():
    """Root endpoint returning API information"""
    return jsonify({
        "name": "ZPodcast API",
        "version": "1.0.0",
        "endpoints": {
            "podcasts": "/api/podcasts/",
            "playlists": "/api/playlists/",
            "episodes": "/api/episodes/"
        },
        "documentation": "/apidocs/"  # Swagger UI endpoint
    })

if __name__ == '__main__':
    app.run(debug=True)
