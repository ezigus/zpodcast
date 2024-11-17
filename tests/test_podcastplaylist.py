import pytest
from zpodcast.podcastplaylist import PodcastPlaylist
from zpodcast.podcastepisode import PodcastEpisode

def test_add_podcastepisode():
    playlist = PodcastPlaylist(name="Test Playlist", episodes=[])
    episode = PodcastEpisode(title="Episode 1", audio_url="https://example.com/episode1.mp3")
    playlist.add_podcastepisode(episode)
    assert len(playlist.episodes) == 1
    assert playlist.episodes[0] == episode

def test_remove_podcastepisode():
    episode1 = PodcastEpisode(title="Episode 1", audio_url="https://example.com/episode1.mp3")
    episode2 = PodcastEpisode(title="Episode 2", audio_url="https://example.com/episode2.mp3")
    playlist = PodcastPlaylist(name="Test Playlist", episodes=[episode1, episode2])
    playlist.remove_podcastepisode(0)
    assert len(playlist.episodes) == 1
    assert playlist.episodes[0] == episode2