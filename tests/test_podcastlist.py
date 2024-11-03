import pytest
from unittest.mock import Mock
from zpodcast.podcastlist import PodcastList
from zpodcast.podcastepisode import PodcastEpisode

def test_sort_playlists_by_date_created():
    episode1 = Mock(spec=PodcastEpisode, pub_date="2023-01-01")
    episode2 = Mock(spec=PodcastEpisode, pub_date="2023-01-02")
    episode3 = Mock(spec=PodcastEpisode, pub_date="2023-01-03")
    playlist = PodcastList(episodes=[episode3, episode1, episode2])
    playlist.sort_playlists("date_created")
    assert playlist.episodes == [episode1, episode2, episode3]

def test_sort_playlists_by_length():
    episode1 = Mock(spec=PodcastEpisode, duration=30)
    episode2 = Mock(spec=PodcastEpisode, duration=60)
    episode3 = Mock(spec=PodcastEpisode, duration=90)
    playlist = PodcastList(episodes=[episode3, episode1, episode2])
    playlist.sort_playlists("length")
    assert playlist.episodes == [episode1, episode2, episode3]

def test_sort_playlists_by_priority():
    episode1 = Mock(spec=PodcastEpisode, priority=1)
    episode2 = Mock(spec=PodcastEpisode, priority=2)
    episode3 = Mock(spec=PodcastEpisode, priority=3)
    playlist = PodcastList(episodes=[episode3, episode1, episode2])
    playlist.sort_playlists("priority")
    assert playlist.episodes == [episode1, episode2, episode3]

def test_sort_playlists_invalid_criteria():
    episode1 = Mock(spec=PodcastEpisode, pub_date="2023-01-01")
    episode2 = Mock(spec=PodcastEpisode, pub_date="2023-01-02")
    episode3 = Mock(spec=PodcastEpisode, pub_date="2023-01-03")
    playlist = PodcastList(episodes=[episode3, episode1, episode2])
    with pytest.raises(ValueError, match="Invalid sorting criteria"):
        playlist.sort_playlists("invalid_criteria")
