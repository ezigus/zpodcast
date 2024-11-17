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

def test_move_episode_up():
    episode1 = PodcastEpisode(title="Episode 1", audio_url="https://example.com/episode1.mp3")
    episode2 = PodcastEpisode(title="Episode 2", audio_url="https://example.com/episode2.mp3")
    episode3 = PodcastEpisode(title="Episode 3", audio_url="https://example.com/episode3.mp3")
    playlist = PodcastPlaylist(name="Test Playlist", episodes=[episode1, episode2, episode3])
    playlist.move_episode_up(2)
    assert playlist.episodes[1] == episode3
    assert playlist.episodes[2] == episode2

def test_move_episode_down():
    episode1 = PodcastEpisode(title="Episode 1", audio_url="https://example.com/episode1.mp3")
    episode2 = PodcastEpisode(title="Episode 2", audio_url="https://example.com/episode2.mp3")
    episode3 = PodcastEpisode(title="Episode 3", audio_url="https://example.com/episode3.mp3")
    playlist = PodcastPlaylist(name="Test Playlist", episodes=[episode1, episode2, episode3])
    playlist.move_episode_down(0)
    assert playlist.episodes[0] == episode2
    assert playlist.episodes[1] == episode1

def test_move_episode_to_position():
    episode1 = PodcastEpisode(title="Episode 1", audio_url="https://example.com/episode1.mp3")
    episode2 = PodcastEpisode(title="Episode 2", audio_url="https://example.com/episode2.mp3")
    episode3 = PodcastEpisode(title="Episode 3", audio_url="https://example.com/episode3.mp3")
    playlist = PodcastPlaylist(name="Test Playlist", episodes=[episode1, episode2, episode3])
    playlist.move_episode_to_position(0, 2)
    assert playlist.episodes[0] == episode2
    assert playlist.episodes[2] == episode1
