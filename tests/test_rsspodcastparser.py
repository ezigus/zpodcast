import pytest
from zpodcast.rsspodcastparser import RSSPodcastParser

def test_parse_episode_length():
    entry = {
        'itunes_duration': '00:30:00'
    }
    length = RSSPodcastParser.parse_episode_length(entry)
    assert length == 1800

def test_parse_episode_length_no_duration():
    entry = {}
    length = RSSPodcastParser.parse_episode_length(entry)
    assert length == 0
