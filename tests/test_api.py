import pytest
from flask import Flask, jsonify
from zpodcast.podcastlist import PodcastList
from zpodcast.podcastplaylist import PodcastPlaylist
from zpodcast.podcastdata import PodcastData

app = Flask(__name__)

@app.route('/api/podcasts', methods=['GET'])
def get_podcasts():
    podcast_list = PodcastList()
    return jsonify(podcast_list.to_dict())

@app.route('/api/playlists', methods=['GET'])
def get_playlists():
    playlist = PodcastPlaylist()
    return jsonify(playlist.to_dict())

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_podcasts(client):
    response = client.get('/api/podcasts')
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert "podcasts" in data

def test_get_playlists(client):
    response = client.get('/api/playlists')
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert "playlists" in data
