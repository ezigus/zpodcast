import pytest
from unittest.mock import Mock
from zpodcast.podcastplaylist import PodcastPlaylist
from zpodcast.podcastepisode import PodcastEpisode

def test_play_episode():
    episode = Mock(spec=PodcastEpisode)
    playlist = PodcastPlaylist(name="Test Playlist", episodes=[episode])
    playlist.play_episode(0)
    episode.play.assert_called_once()

def test_play_playlist():
    episode1 = Mock(spec=PodcastEpisode)
    episode2 = Mock(spec=PodcastEpisode)
    playlist = PodcastPlaylist(name="Test Playlist", episodes=[episode1, episode2])
    playlist.play_playlist()
    episode1.play.assert_called_once()
    episode2.play.assert_called_once()

def test_display_remaining_time_playlist():
    episode1 = Mock(spec=PodcastEpisode, duration=30, is_listened=False)
    episode2 = Mock(spec=PodcastEpisode, duration=60, is_listened=True)
    episode3 = Mock(spec=PodcastEpisode, duration=90, is_listened=False)
    playlist = PodcastPlaylist(name="Test Playlist", episodes=[episode1, episode2, episode3])
    remaining_time = playlist.display_remaining_time_playlist()
    assert remaining_time == 120

def test_remove_listened_episode():
    episode1 = Mock(spec=PodcastEpisode, is_listened=False)
    episode2 = Mock(spec=PodcastEpisode, is_listened=True)
    episode3 = Mock(spec=PodcastEpisode, is_listened=False)
    playlist = PodcastPlaylist(name="Test Playlist", episodes=[episode1, episode2, episode3])
    playlist.remove_listened_episode()
    assert playlist.episodes == [episode1, episode3]
