import pytest
import os
import tempfile
import shutil
from flask import jsonify
from zpodcast.api.app import zPodcastApp
from zpodcast.core.podcasts import PodcastList, PodcastData
from zpodcast.core.playlists import PodcastPlaylist
from zpodcast.parsers.json import PodcastJSON
from unittest.mock import patch


@pytest.fixture
def test_data_dir():
    """Get the path to the test data directory"""
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


@pytest.fixture
def temp_data_dir():
    """Create a temporary data directory with test files"""
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()

    # Copy test data files to the temporary directory
    test_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    for filename in ["podcast_list.json", "podcast_playlist.json"]:
        src = os.path.join(test_dir, filename)
        if os.path.exists(src):
            dst = os.path.join(temp_dir, filename)
            shutil.copy2(src, dst)

    yield temp_dir

    # Clean up the temporary directory
    shutil.rmtree(temp_dir)


@pytest.fixture
def mock_rss_calls():
    """Mock the RSS-related calls to prevent external network requests"""
    # Simple patch of the RSS methods that would try to access external URLs
    with patch(
        "zpodcast.parsers.rss.RSSPodcastParser.get_episodes", return_value=[]
    ), patch("zpodcast.parsers.rss.RSSPodcastParser.get_rss_metadata", return_value={}):
        yield


@pytest.fixture
def real_app(test_data_dir, mock_rss_calls):
    """Create a Flask app using actual test data files"""
    podcast_app = zPodcastApp()
    app = podcast_app.create_app(test_data_dir)
    app.config["TESTING"] = True

    # Ensure the index route is defined
    @app.route("/")
    def index():
        return jsonify(
            {
                "name": "ZPodcast API",
                "version": "1.0.0",
                "endpoints": {
                    "podcasts": "/api/podcasts",
                    "playlists": "/api/playlists",
                    "episodes": "/api/episodes",
                },
            }
        )

    return app


@pytest.fixture
def real_client(real_app):
    """Create a test client for the Flask app with real data"""
    return real_app.test_client()


@pytest.fixture
def modifiable_app(temp_data_dir, mock_rss_calls):
    """Create a Flask app with a modifiable temp data directory"""
    podcast_app = zPodcastApp()
    app = podcast_app.create_app(temp_data_dir)
    app.config["TESTING"] = True

    # Ensure the index route is defined
    @app.route("/")
    def index():
        return jsonify(
            {
                "name": "ZPodcast API",
                "version": "1.0.0",
                "endpoints": {
                    "podcasts": "/api/podcasts",
                    "playlists": "/api/playlists",
                    "episodes": "/api/episodes",
                },
            }
        )

    return app


@pytest.fixture
def modifiable_client(modifiable_app):
    """Create a test client for the Flask app with modifiable data"""
    return modifiable_app.test_client()


def test_real_app_initialization(real_app, test_data_dir):
    """Test that the app initializes correctly with real files"""
    # Check basic configuration
    assert real_app.config["DATA_DIR"] == test_data_dir
    assert "podcast_list" in real_app.config
    assert "podcast_playlist" in real_app.config

    # Verify the objects were properly loaded from files
    assert isinstance(real_app.config["podcast_list"], PodcastList)
    assert isinstance(real_app.config["podcast_playlist"], PodcastPlaylist)


def test_app_loads_correct_podcast_data(real_app):
    """Test that the app loads the correct podcast data from files"""
    podcast_list = real_app.config["podcast_list"]

    # Verify that podcasts were loaded
    assert len(podcast_list.podcasts) > 0

    # Verify basic properties of the first podcast
    first_podcast = podcast_list.podcasts[0]
    assert isinstance(first_podcast, PodcastData)
    assert isinstance(first_podcast.title, str)
    assert isinstance(first_podcast.podcast_url, str)


def test_app_loads_correct_playlist_data(real_app):
    """Test that the app loads the correct playlist data from files"""
    playlist = real_app.config["podcast_playlist"]

    # Verify that playlists were loaded
    assert isinstance(playlist, PodcastPlaylist)
    assert hasattr(playlist, "playlists")

    # Note: The actual number of playlists might vary depending on test data


def test_api_endpoints_with_real_data(real_client):
    """Test the API endpoints with real data"""
    # Test podcasts endpoint
    response = real_client.get("/api/podcasts/")
    assert response.status_code == 200
    data = response.get_json()
    assert "podcasts" in data

    # Test playlists endpoint
    response = real_client.get("/api/playlists/")
    assert response.status_code == 200
    data = response.get_json()
    assert "playlists" in data


def test_modified_data_persistence(temp_data_dir, mock_rss_calls):
    """Test that modified data can be correctly saved and loaded"""
    # Create the first app and get its podcast list
    with patch("zpodcast.core.podcast.PodcastData.populate_episodes_from_feed"):
        first_app = zPodcastApp().create_app(temp_data_dir)
        podcast_list = first_app.config["podcast_list"]
        initial_count = len(podcast_list.podcasts)

        # Create a new podcast
        new_podcast = PodcastData(
            title="Integration Test Podcast",
            podcast_url="http://example.com/integration.rss",
            host="Integration Tester",
            description="A podcast for integration testing",
            episodelists=[],
            podcast_priority=3,
            image_url="http://example.com/integration.jpg",
        )

        # Add it to the list
        podcast_list.add_podcast(new_podcast)

        # Save the modified podcast list to JSON
        podcast_list_path = os.path.join(temp_data_dir, "podcast_list.json")
        PodcastJSON.export_podcast_list(podcast_list, podcast_list_path)

        # Create a new app to load the saved data
        second_app = zPodcastApp().create_app(temp_data_dir)

        # Verify the new podcast was saved and loaded
        new_podcast_list = second_app.config["podcast_list"]
        assert len(new_podcast_list.podcasts) == initial_count + 1

        # Find our podcast by title
        found_podcasts = [
            p
            for p in new_podcast_list.podcasts
            if p.title == "Integration Test Podcast"
        ]
        assert len(found_podcasts) == 1

        # Verify the properties are correct
        found_podcast = found_podcasts[0]
        assert found_podcast.title == "Integration Test Podcast"
        assert found_podcast.podcast_url == "http://example.com/integration.rss"
        assert found_podcast.description == "A podcast for integration testing"
        assert found_podcast.podcast_priority == 3
        assert found_podcast.host == "Integration Tester"
