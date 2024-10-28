import pytest
import os
from zpodcast.podcastplaylist import PodcastPlaylist
from zpodcast.podcastepisode import PodcastEpisode
from datetime import datetime

@pytest.fixture
def sample_episodes():
    return [
        PodcastEpisode(
            title="Episode 1",
            description="Description 1",
            audio_url="https://example.com/episode1.mp3",
            pub_date=datetime(2023, 1, 1),
            duration=1800,
            episode_number=1,
            image_url="https://example.com/episode1.jpg"
        ),
        PodcastEpisode(
            title="Episode 2",
            description="Description 2",
            audio_url="https://example.com/episode2.mp3",
            pub_date=datetime(2023, 1, 2),
            duration=3600,
            episode_number=2,
            image_url="https://example.com/episode2.jpg"
        )
    ]

def test_create_playlist(sample_episodes):
    playlist = PodcastPlaylist(name="Test Playlist", episodes=[])
    playlist.create_playlist(name="New Playlist", episodes=sample_episodes)
    
    assert playlist.name == "New Playlist"
    assert len(playlist.episodes) == 2
    assert playlist.episodes[0].title == "Episode 1"
    assert playlist.episodes[1].title == "Episode 2"

def test_save_playlist(sample_episodes, tmp_path):
    playlist = PodcastPlaylist(name="Test Playlist", episodes=sample_episodes)
    file_path = tmp_path / "playlist.json"
    playlist.save_playlist(file_path)
    
    assert os.path.exists(file_path)

def test_load_playlist(tmp_path):
    file_path = tmp_path / "playlist.json"
    with open(file_path, 'w') as file:
        file.write('{"name": "Loaded Playlist", "episodes": [{"title": "Episode 1", "description": "Description 1", "audio_url": "https://example.com/episode1.mp3", "pub_date": "2023-01-01T00:00:00", "duration": 1800, "episode_number": 1, "image_url": "https://example.com/episode1.jpg"}, {"title": "Episode 2", "description": "Description 2", "audio_url": "https://example.com/episode2.mp3", "pub_date": "2023-01-02T00:00:00", "duration": 3600, "episode_number": 2, "image_url": "https://example.com/episode2.jpg"}]}')
    
    playlist = PodcastPlaylist(name="", episodes=[])
    playlist.load_playlist(file_path)
    
    assert playlist.name == "Loaded Playlist"
    assert len(playlist.episodes) == 2
    assert playlist.episodes[0].title == "Episode 1"
    assert playlist.episodes[1].title == "Episode 2"
