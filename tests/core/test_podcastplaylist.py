import pytest
from zpodcast.core.playlists import PodcastPlaylist
from zpodcast.core.playlist import PodcastEpisodeList
from zpodcast.core.episode import PodcastEpisode
from datetime import date

def test_add_playlist():
    playlist = PodcastEpisodeList(name="Test Playlist", episodes=[])
    podcast_playlist = PodcastPlaylist(playlists=[])
    podcast_playlist.add_playlist(playlist)
    assert len(podcast_playlist.playlists) == 1
    assert podcast_playlist.playlists[0] == playlist

def test_remove_playlist():
    playlist1 = PodcastEpisodeList(name="Test Playlist 1", episodes=[])
    playlist2 = PodcastEpisodeList(name="Test Playlist 2", episodes=[])
    podcast_playlist = PodcastPlaylist(playlists=[playlist1, playlist2])
    podcast_playlist.remove_playlist(0)
    assert len(podcast_playlist.playlists) == 1
    assert podcast_playlist.playlists[0] == playlist2

def test_get_playlist():
    playlist1 = PodcastEpisodeList(name="Test Playlist 1", episodes=[])
    playlist2 = PodcastEpisodeList(name="Test Playlist 2", episodes=[])
    podcast_playlist = PodcastPlaylist(playlists=[playlist1, playlist2])
    playlist = podcast_playlist.get_playlist(1)
    assert playlist == playlist2

def test_get_all_playlists():
    playlist1 = PodcastEpisodeList(name="Test Playlist 1", episodes=[])
    playlist2 = PodcastEpisodeList(name="Test Playlist 2", episodes=[])
    podcast_playlist = PodcastPlaylist(playlists=[playlist1, playlist2])
    playlists = podcast_playlist.get_all_playlists()
    assert len(playlists) == 2
    assert playlists[0] == playlist1
    assert playlists[1] == playlist2

def test_to_dict():
    episode1 = PodcastEpisode(title="Episode 1", audio_url="https://example.com/episode1.mp3")
    episode2 = PodcastEpisode(title="Episode 2", audio_url="https://example.com/episode2.mp3")
    playlist1 = PodcastEpisodeList(name="Test Playlist 1", episodes=[episode1])
    playlist2 = PodcastEpisodeList(name="Test Playlist 2", episodes=[episode2])
    podcast_playlist = PodcastPlaylist(playlists=[playlist1, playlist2])
    podcast_playlist_dict = podcast_playlist.to_dict()
    assert podcast_playlist_dict == {
        "playlists": [
            {
                "name": "Test Playlist 1",
                "episodes": [
                    {
                        "title": "Episode 1",
                        "audio_url": "https://example.com/episode1.mp3",
                        "description": "",
                        "pub_date": date.today().isoformat(),
                        "duration": None,
                        "episode_number": None,
                        "image_url": None
                    }
                ]
            },
            {
                "name": "Test Playlist 2",
                "episodes": [
                    {
                        "title": "Episode 2",
                        "audio_url": "https://example.com/episode2.mp3",
                        "description": "",
                        "pub_date": date.today().isoformat(),
                        "duration": None,
                        "episode_number": None,
                        "image_url": None
                    }
                ]
            }
        ]
    }

def test_from_dict():
    podcast_playlist_dict = {
        "playlists": [
            {
                "name": "Test Playlist 1",
                "episodes": [
                    {
                        "title": "Episode 1",
                        "audio_url": "https://example.com/episode1.mp3",
                        "description": "",
                        "pub_date": date.today().isoformat(),
                        "duration": None,
                        "episode_number": None,
                        "image_url": None
                    }
                ]
            },
            {
                "name": "Test Playlist 2",
                "episodes": [
                    {
                        "title": "Episode 2",
                        "audio_url": "https://example.com/episode2.mp3",
                        "description": "",
                        "pub_date": date.today().isoformat(),
                        "duration": None,
                        "episode_number": None,
                        "image_url": None
                    }
                ]
            }
        ]
    }
    podcast_playlist = PodcastPlaylist.from_dict(podcast_playlist_dict)
    assert len(podcast_playlist.playlists) == 2
    assert podcast_playlist.playlists[0].name == "Test Playlist 1"
    assert podcast_playlist.playlists[1].name == "Test Playlist 2"
