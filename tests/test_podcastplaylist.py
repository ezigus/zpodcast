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

def test_get_all_episode_details():
    episode1 = PodcastEpisode(title="Episode 1", audio_url="https://example.com/episode1.mp3", duration=1800)
    episode2 = PodcastEpisode(title="Episode 2", audio_url="https://example.com/episode2.mp3", duration=3600)
    playlist = PodcastPlaylist(name="Test Playlist", episodes=[episode1, episode2])
    details = playlist.get_all_episode_details()
    assert len(details) == 2
    assert details[0]["title"] == "Episode 1"
    assert details[0]["duration"] == 1800
    assert details[0]["audio_url"] == "https://example.com/episode1.mp3"
    assert details[1]["title"] == "Episode 2"
    assert details[1]["duration"] == 3600
    assert details[1]["audio_url"] == "https://example.com/episode2.mp3"

def test_get_episode_details():
    episode1 = PodcastEpisode(title="Episode 1", audio_url="https://example.com/episode1.mp3", duration=1800)
    episode2 = PodcastEpisode(title="Episode 2", audio_url="https://example.com/episode2.mp3", duration=3600)
    playlist = PodcastPlaylist(name="Test Playlist", episodes=[episode1, episode2])
    details = playlist.get_episode_details(1)
    assert details["title"] == "Episode 2"
    assert details["duration"] == 3600
    assert details["audio_url"] == "https://example.com/episode2.mp3"

def test_get_episodes_all():
    episode1 = PodcastEpisode(title="Episode 1", audio_url="https://example.com/episode1.mp3", duration=1800)
    episode2 = PodcastEpisode(title="Episode 2", audio_url="https://example.com/episode2.mp3", duration=3600)
    playlist = PodcastPlaylist(name="Test Playlist", episodes=[episode1, episode2])
    episodes = playlist.get_episodes()
    assert len(episodes) == 2
    assert episodes[0] == episode1
    assert episodes[1] == episode2

def test_get_episodes_specific():
    episode1 = PodcastEpisode(title="Episode 1", audio_url="https://example.com/episode1.mp3", duration=1800)
    episode2 = PodcastEpisode(title="Episode 2", audio_url="https://example.com/episode2.mp3", duration=3600)
    episode3 = PodcastEpisode(title="Episode 3", audio_url="https://example.com/episode3.mp3", duration=5400)
    playlist = PodcastPlaylist(name="Test Playlist", episodes=[episode1, episode2, episode3])
    episodes = playlist.get_episodes([0, 2])
    assert len(episodes) == 2
    assert episodes[0] == episode1
    assert episodes[1] == episode3

def test_get_episodes_invalid_indices():
    episode1 = PodcastEpisode(title="Episode 1", audio_url="https://example.com/episode1.mp3", duration=1800)
    episode2 = PodcastEpisode(title="Episode 2", audio_url="https://example.com/episode2.mp3", duration=3600)
    episode3 = PodcastEpisode(title="Episode 3", audio_url="https://example.com/episode3.mp3", duration=5400)
    playlist = PodcastPlaylist(name="Test Playlist", episodes=[episode1, episode2, episode3])
    with pytest.raises(ValueError):
        episodes = playlist.get_episodes(["a"])


def test_get_episodes_any_order():
    episode1 = PodcastEpisode(title="Episode 1", audio_url="https://example.com/episode1.mp3", duration=1800)
    episode2 = PodcastEpisode(title="Episode 2", audio_url="https://example.com/episode2.mp3", duration=3600)
    episode3 = PodcastEpisode(title="Episode 3", audio_url="https://example.com/episode3.mp3", duration=5400)
    playlist = PodcastPlaylist(name="Test Playlist", episodes=[episode1, episode2, episode3])
    episodes = playlist.get_episodes([1, 2, 1, 0])
    assert len(episodes) == 4
    assert episodes[0] == episode2
    assert episodes[1] == episode3
    assert episodes[2] == episode2
    assert episodes[3] == episode1

def test_get_episodes_too_low():
    episode1 = PodcastEpisode(title="Episode 1", audio_url="https://example.com/episode1.mp3", duration=1800)
    episode2 = PodcastEpisode(title="Episode 2", audio_url="https://example.com/episode2.mp3", duration=3600)
    episode3 = PodcastEpisode(title="Episode 3", audio_url="https://example.com/episode3.mp3", duration=5400)
    playlist = PodcastPlaylist(name="Test Playlist", episodes=[episode1, episode2, episode3])
    with pytest.raises(ValueError):
        episodes = playlist.get_episodes([-1, 2, 0])

def test_get_episodes_too_high():
    episode1 = PodcastEpisode(title="Episode 1", audio_url="https://example.com/episode1.mp3", duration=1800)
    episode2 = PodcastEpisode(title="Episode 2", audio_url="https://example.com/episode2.mp3", duration=3600)
    episode3 = PodcastEpisode(title="Episode 3", audio_url="https://example.com/episode3.mp3", duration=5400)
    playlist = PodcastPlaylist(name="Test Playlist", episodes=[episode1, episode2, episode3])
    with pytest.raises(ValueError):
        episodes = playlist.get_episodes([1, 3, 0])
    