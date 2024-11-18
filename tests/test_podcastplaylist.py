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

def test_set_name():
    playlist = PodcastPlaylist(name="Test Playlist", episodes=[])
    playlist.set_name("New Playlist Name")
    assert playlist.name == "New Playlist Name"

def test_set_name_invalid():
    playlist = PodcastPlaylist(name="Test Playlist", episodes=[])
    with pytest.raises(ValueError):
        playlist.set_name("Invalid@Name")

def test_get_num_items():
    episode1 = PodcastEpisode(title="Episode 1", audio_url="https://example.com/episode1.mp3")
    episode2 = PodcastEpisode(title="Episode 2", audio_url="https://example.com/episode2.mp3")
    playlist = PodcastPlaylist(name="Test Playlist", episodes=[episode1, episode2])
    assert playlist.get_num_items() == 2

def test_calculate_duration():
    episode1 = PodcastEpisode(title="Episode 1", audio_url="https://example.com/episode1.mp3", duration=1800)
    episode2 = PodcastEpisode(title="Episode 2", audio_url="https://example.com/episode2.mp3", duration=3600)
    playlist = PodcastPlaylist(name="Test Playlist", episodes=[episode1, episode2])
    assert playlist.calculate_duration() == 5400

def test_format_duration():
    playlist = PodcastPlaylist(name="Test Playlist", episodes=[])
    formatted_duration = playlist._format_duration(5400)
    assert formatted_duration == "0 days, 01:30:00"
    
def test_format_duration_seconds():
    playlist = PodcastPlaylist(name="Test Playlist", episodes=[])
    formatted_duration = playlist._format_duration(5401)
    assert formatted_duration == "0 days, 01:30:01"
    
def test_format_duration_minutes():
    playlist = PodcastPlaylist(name="Test Playlist", episodes=[])
    formatted_duration = playlist._format_duration(5461)
    assert formatted_duration == "0 days, 01:31:01"
    
def test_format_duration_days():
    playlist = PodcastPlaylist(name="Test Playlist", episodes=[])
    formatted_duration = playlist._format_duration(90061)
    assert formatted_duration == "1 days, 01:01:01"
    

def test_convert_duration_to_string():
    playlist = PodcastPlaylist(name="Test Playlist", episodes=[])
    duration_string = playlist.convert_duration_to_string(5400)
    assert duration_string == "0 days, 01:30:00"
