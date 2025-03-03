import pytest
from flask import Flask, jsonify
from zpodcast.app import PodcastApp

@pytest.fixture
def client():
    podcast_app = PodcastApp()
    app = podcast_app.create_app()
    with app.test_client() as client:
        yield client

def test_get_podcasts(client):
    response = client.get('/podcasts')
    assert response.status_code == 200
    data = response.get_json()
    assert 'podcasts' in data

def test_get_playlists(client):
    response = client.get('/playlists')
    assert response.status_code == 200
    data = response.get_json()
    assert 'playlists' in data
