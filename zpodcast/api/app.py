"""
ZPodcast API Application

This module initializes the Flask application for the ZPodcast API. It sets up
blueprints, error handlers, and Swagger documentation. The application is
responsible for managing podcasts, playlists, and episodes.

Classes:
    zPodcastApp: Encapsulates the Flask application setup and configuration.

Functions:
    index: Root endpoint providing API information.

"""

from typing import Any

from flask import Flask, jsonify
from flasgger import Swagger, swag_from

from zpodcast.api.blueprints import podcasts_bp, playlists_bp, episodes_bp
from zpodcast.parsers.json import PodcastJSON

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

swagger_template['paths'] = {
    '/': {
        'get': {
            'summary': 'Root endpoint providing API metadata',
            'description': 'Returns API metadata including available endpoints and documentation link.',
            'responses': {
                '200': {
                    'description': 'API metadata',
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'name': {'type': 'string', 'description': 'API name'},
                            'version': {'type': 'string', 'description': 'API version'},
                            'endpoints': {
                                'type': 'object',
                                'description': 'Available API endpoints',
                                'properties': {
                                    'podcasts': {'type': 'string', 'description': 'Podcasts endpoint'},
                                    'playlists': {'type': 'string', 'description': 'Playlists endpoint'},
                                    'episodes': {'type': 'string', 'description': 'Episodes endpoint'}
                                }
                            },
                            'documentation': {'type': 'string', 'description': 'Swagger UI endpoint'}
                        },
                        'required': ['name', 'version', 'endpoints', 'documentation']
                    }
                }
            },
            'tags': ['root']
        }
    },
    '/api/playlists/': {
        'get': {
            'summary': 'Retrieve all playlists',
            'description': 'Fetches a list of all playlists.',
            'responses': {
                '200': {'description': 'List of playlists'},
                '500': {'description': 'Server error'}
            },
            'tags': ['playlists']
        },
        'post': {
            'summary': 'Create a new playlist',
            'description': 'Adds a new playlist to the system.',
            'responses': {
                '201': {'description': 'Playlist created'},
                '400': {'description': 'Invalid input'},
                '500': {'description': 'Server error'}
            },
            'tags': ['playlists']
        }
    },
    '/api/episodes/': {
        'get': {
            'summary': 'Retrieve all episodes',
            'description': 'Fetches a list of all episodes.',
            'responses': {
                '200': {'description': 'List of episodes'},
                '500': {'description': 'Server error'}
            },
            'tags': ['episodes']
        },
        'post': {
            'summary': 'Create a new episode',
            'description': 'Adds a new episode to the system.',
            'responses': {
                '201': {'description': 'Episode created'},
                '400': {'description': 'Invalid input'},
                '500': {'description': 'Server error'}
            },
            'tags': ['episodes']
        }
    }
}

swagger_template['paths']['/api/playlists/{playlist_id}/'] = {
    'get': {
        'summary': 'Retrieve a specific playlist',
        'description': 'Fetches details of a specific playlist by its ID.',
        'parameters': [
            {
                'name': 'playlist_id',
                'in': 'path',
                'required': True,
                'type': 'integer',
                'description': 'Unique identifier of the playlist'
            }
        ],
        'responses': {
            '200': {'description': 'Playlist details'},
            '404': {'description': 'Playlist not found'},
            '500': {'description': 'Server error'}
        },
        'tags': ['playlists']
    },
    'put': {
        'summary': 'Update a specific playlist',
        'description': 'Updates details of a specific playlist by its ID.',
        'parameters': [
            {
                'name': 'playlist_id',
                'in': 'path',
                'required': True,
                'type': 'integer',
                'description': 'Unique identifier of the playlist'
            }
        ],
        'responses': {
            '200': {'description': 'Playlist updated'},
            '400': {'description': 'Invalid input'},
            '404': {'description': 'Playlist not found'},
            '500': {'description': 'Server error'}
        },
        'tags': ['playlists']
    },
    'delete': {
        'summary': 'Delete a specific playlist',
        'description': 'Deletes a specific playlist by its ID.',
        'parameters': [
            {
                'name': 'playlist_id',
                'in': 'path',
                'required': True,
                'type': 'integer',
                'description': 'Unique identifier of the playlist'
            }
        ],
        'responses': {
            '204': {'description': 'Playlist deleted'},
            '404': {'description': 'Playlist not found'},
            '500': {'description': 'Server error'}
        },
        'tags': ['playlists']
    }
}

swagger_template['paths']['/api/episodes/{episode_id}/'] = {
    'get': {
        'summary': 'Retrieve a specific episode',
        'description': 'Fetches details of a specific episode by its ID.',
        'parameters': [
            {
                'name': 'episode_id',
                'in': 'path',
                'required': True,
                'type': 'integer',
                'description': 'Unique identifier of the episode'
            }
        ],
        'responses': {
            '200': {'description': 'Episode details'},
            '404': {'description': 'Episode not found'},
            '500': {'description': 'Server error'}
        },
        'tags': ['episodes']
    },
    'put': {
        'summary': 'Update a specific episode',
        'description': 'Updates details of a specific episode by its ID.',
        'parameters': [
            {
                'name': 'episode_id',
                'in': 'path',
                'required': True,
                'type': 'integer',
                'description': 'Unique identifier of the episode'
            }
        ],
        'responses': {
            '200': {'description': 'Episode updated'},
            '400': {'description': 'Invalid input'},
            '404': {'description': 'Episode not found'},
            '500': {'description': 'Server error'}
        },
        'tags': ['episodes']
    },
    'delete': {
        'summary': 'Delete a specific episode',
        'description': 'Deletes a specific episode by its ID.',
        'parameters': [
            {
                'name': 'episode_id',
                'in': 'path',
                'required': True,
                'type': 'integer',
                'description': 'Unique identifier of the episode'
            }
        ],
        'responses': {
            '204': {'description': 'Episode deleted'},
            '404': {'description': 'Episode not found'},
            '500': {'description': 'Server error'}
        },
        'tags': ['episodes']
    }
}


class zPodcastApp:
    def __init__(self):
        self.app: Flask = Flask(__name__)
        self._register_blueprints()
        self._setup_error_handlers()

    def _register_blueprints(self) -> None:
        """Register all blueprints with their respective URL prefixes."""
        self.app.register_blueprint(podcasts_bp, url_prefix='/api/podcasts/')
        self.app.register_blueprint(playlists_bp, url_prefix='/api/playlists/')
        self.app.register_blueprint(episodes_bp, url_prefix='/api/episodes/')

    def _setup_error_handlers(self) -> None:
        """Setup error handlers for common HTTP errors."""
        @self.app.errorhandler(404)
        def not_found_error(error: Any) -> Any:
            return jsonify({"error": "Resource not found"}), 404

        @self.app.errorhandler(400)
        def bad_request_error(error: Any) -> Any:
            return jsonify({"error": "Bad request"}), 400

        @self.app.errorhandler(500)
        def internal_server_error(error: Any) -> Any:
            return jsonify({"error": "Internal server error"}), 500

    def create_app(self, data_dir: str) -> Flask:
        """
        Create and configure the Flask application.

        Args:
            data_dir (str): Path to the directory containing podcast data files.

        Returns:
            Flask: Configured Flask application instance.
        """
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
    def create_app_factory(data_dir: str) -> Flask:
        """
        Factory function to create the application.

        Args:
            data_dir (str): Path to the directory containing podcast data files.

        Returns:
            Flask: Configured Flask application instance.
        """
        app = zPodcastApp()
        return app.create_app(data_dir)


# Create the application instance
app = zPodcastApp().create_app(os.getenv('ZPODCAST_DATA_DIR', 'data'))


@app.route('/')
@swag_from({
    'responses': {
        200: {
            'description': 'API metadata including available endpoints and documentation link',
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string', 'description': 'API name'},
                    'version': {'type': 'string', 'description': 'API version'},
                    'endpoints': {
                        'type': 'object',
                        'description': 'Available API endpoints',
                        'properties': {
                            'podcasts': {'type': 'string', 'description': 'Podcasts endpoint'},
                            'playlists': {'type': 'string', 'description': 'Playlists endpoint'},
                            'episodes': {'type': 'string', 'description': 'Episodes endpoint'}
                        }
                    },
                    'documentation': {'type': 'string', 'description': 'Swagger UI endpoint'}
                },
                'required': ['name', 'version', 'endpoints', 'documentation']
            }
        }
    },
    'summary': 'Root endpoint providing API metadata',
    'tags': ['root']
})
def index() -> Any:
    """
    Root endpoint returning API information.

    Returns:
        JSON: API metadata including available endpoints and documentation link.
    """
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
