import pytest
from flask import Flask
from zpodcast.api.blueprints.playlists import playlists_bp
from zpodcast.core.playlists import PodcastPlaylist
from zpodcast.core.playlist import PodcastEpisodeList
from zpodcast.core.episode import PodcastEpisode


@pytest.fixture
def test_playlist_data(mocker):
    """Create test playlist data for testing"""
    episodes1 = [
        PodcastEpisode(
            title="Test Episode 1",
            audio_url="https://example.com/episode1.mp3",
            description="Test episode 1 description",
            duration=1800,
        ),
        PodcastEpisode(
            title="Test Episode 2",
            audio_url="https://example.com/episode2.mp3",
            description="Test episode 2 description",
            duration=2400,
        ),
    ]

    episodes2 = [
        PodcastEpisode(
            title="Test Episode 3",
            audio_url="https://example.com/episode3.mp3",
            description="Test episode 3 description",
            duration=1500,
        )
    ]

    return [
        PodcastEpisodeList(name="Test Playlist 1", episodes=episodes1),
        PodcastEpisodeList(name="Test Playlist 2", episodes=episodes2),
    ]


@pytest.fixture
def app(mocker, test_playlist_data):
    """Set up a Flask app with the playlists blueprint registered"""
    app = Flask(__name__)

    # Create a consistent test PodcastPlaylist
    podcast_playlist = PodcastPlaylist(test_playlist_data)

    # Patch the get_instance method
    mocker.patch(
        "zpodcast.core.playlists.PodcastPlaylist.get_instance",
        return_value=podcast_playlist,
    )
    mocker.patch(
        "zpodcast.api.blueprints.playlists.PodcastPlaylist.get_instance",
        return_value=podcast_playlist,
    )

    # Register blueprint
    app.register_blueprint(playlists_bp, url_prefix="/api/playlists")

    return app


@pytest.fixture
def client(app):
    """Create a test client for the Flask app"""
    return app.test_client()


def test_get_playlists(client):
    """Test getting all playlists through the blueprint"""
    response = client.get("/api/playlists/")
    assert response.status_code == 200
    data = response.get_json()
    assert "playlists" in data
    assert len(data["playlists"]) == 2
    assert data["playlists"][0]["name"] == "Test Playlist 1"
    assert data["playlists"][1]["name"] == "Test Playlist 2"


def test_get_playlist_by_id(client):
    """Test getting a specific playlist by ID through the blueprint"""
    response = client.get("/api/playlists/0/")  # First playlist
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Test Playlist 1"
    assert len(data["episodes"]) == 2


def test_get_playlist_by_id_not_found(client):
    """Test getting a non-existent playlist ID through the blueprint"""
    response = client.get("/api/playlists/999/")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Playlist not found"


def test_create_playlist(client, mocker, test_playlist_data):
    """Test creating a new playlist"""
    # Set up the test PodcastPlaylist as a mutable fixture that will be modified
    podcast_playlist = PodcastPlaylist(test_playlist_data.copy())
    mocker.patch(
        "zpodcast.api.blueprints.playlists.PodcastPlaylist.get_instance",
        return_value=podcast_playlist,
    )

    new_playlist_data = {"name": "New Playlist"}
    response = client.post("/api/playlists/", json=new_playlist_data)
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "New Playlist"
    assert "episodes" in data


def test_create_playlist_no_data(client):
    """Test creating a playlist with no data"""
    response = client.post("/api/playlists/", json={})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "No data provided"


def test_update_playlist(client, mocker, test_playlist_data):
    """Test updating a playlist"""
    # Set up the test PodcastPlaylist as a mutable fixture that will be modified
    podcast_playlist = PodcastPlaylist(test_playlist_data.copy())
    mocker.patch(
        "zpodcast.api.blueprints.playlists.PodcastPlaylist.get_instance",
        return_value=podcast_playlist,
    )

    update_data = {"name": "Updated Playlist"}
    response = client.put("/api/playlists/0/", json=update_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Updated Playlist"


def test_update_playlist_no_data(client):
    """Test updating a playlist with no data"""
    response = client.put("/api/playlists/0/", json={})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "No data provided"


def test_delete_playlist(client, mocker, test_playlist_data):
    """Test removing a playlist"""
    # Create a fresh playlist for this test
    podcast_playlist = PodcastPlaylist(test_playlist_data.copy())

    # Create a consistent mock that will be used throughout the test
    mocker.patch(
        "zpodcast.api.blueprints.playlists.PodcastPlaylist.get_instance",
        return_value=podcast_playlist,
    )

    # First verify the playlist exists
    response = client.get("/api/playlists/0/")
    assert response.status_code == 200
    first_id_data = response.get_json()
    assert first_id_data["name"] == "Test Playlist 1"

    # Then delete it
    response = client.delete("/api/playlists/0/")
    assert response.status_code == 204

    # Verify that index 0 now contains what was previously at index 1
    response = client.get("/api/playlists/0/")
    assert response.status_code == 200
    new_first_data = response.get_json()
    assert new_first_data["name"] == "Test Playlist 2"

    # Verify that the list now has one less playlist
    response = client.get("/api/playlists/")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data["playlists"]) == 1


def test_delete_playlist_not_found(client):
    """Test removing a non-existent playlist"""
    response = client.delete("/api/playlists/999/")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data


def test_add_episode_to_playlist(client, mocker, test_playlist_data):
    """Test adding an episode to a playlist"""
    # Set up the test PodcastPlaylist as a mutable fixture that will be modified
    podcast_playlist = PodcastPlaylist(test_playlist_data.copy())
    mocker.patch(
        "zpodcast.api.blueprints.playlists.PodcastPlaylist.get_instance",
        return_value=podcast_playlist,
    )

    # Get the current playlist to compare after adding episode
    response = client.get("/api/playlists/0/")
    assert response.status_code == 200
    original_data = response.get_json()
    original_episode_count = len(original_data["episodes"])

    episode_data = {
        "title": "New Episode",
        "audio_url": "https://example.com/new-episode.mp3",
        "description": "New episode description",
        "duration": 1800,
    }
    response = client.post("/api/playlists/0/episodes/", json=episode_data)
    assert response.status_code == 200
    data = response.get_json()
    assert len(data["episodes"]) > original_episode_count
    assert any(episode["title"] == "New Episode" for episode in data["episodes"])


def test_add_episode_to_playlist_no_data(client):
    """Test adding an episode to a playlist with no data"""
    response = client.post("/api/playlists/0/episodes/", json={})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "No data provided"


def test_remove_episode_from_playlist(client, mocker, test_playlist_data):
    """Test removing an episode from a playlist"""
    # Set up the test PodcastPlaylist as a mutable fixture that will be modified
    podcast_playlist = PodcastPlaylist(test_playlist_data.copy())
    mocker.patch(
        "zpodcast.api.blueprints.playlists.PodcastPlaylist.get_instance",
        return_value=podcast_playlist,
    )

    # Get the current playlist to compare after removing episode
    response = client.get("/api/playlists/0/")
    assert response.status_code == 200
    original_data = response.get_json()
    original_episode_count = len(original_data["episodes"])
    assert original_episode_count > 0

    response = client.delete("/api/playlists/0/episodes/0/")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data["episodes"]) < original_episode_count


def test_remove_episode_from_playlist_not_found(client):
    """Test removing a non-existent episode from a playlist"""
    response = client.delete("/api/playlists/0/episodes/999/")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data
