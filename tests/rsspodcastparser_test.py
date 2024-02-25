import pytest
from unittest.mock import patch
from zpodcast.rsspodcastparser import RSSPodcastParser



def test_get_episodes():
    # Mock the feedparser library
    with patch('RSSPodcastParser.feedparser') as mock_feedparser:
        # Create a mock RSS feed
        rss_feed = {
            'entries': [
                {
                    'title': 'Episode 1',
                    'description': 'This is episode 1',
                    'published': '2022-01-01',
                    'itunes_duration': '00:30:00',
                    'enclosures': [{'href': 'audio_url'}],
                    'itunes_episode': '1'
                },
                {
                    'title': 'Episode 2',
                    'description': 'This is episode 2',
                    'published': '2022-01-02',
                    'itunes_duration': '00:45:00',
                    'enclosures': [{'href': 'audio_url'}],
                    'itunes_episode': '2'
                }
            ]
        }
        mock_feedparser.parse.return_value = rss_feed

        # Call the get_episodes method
        episodes = RSSPodcastParser.get_episodes('rss_feed_url')

        # Assert that the episodes are correctly parsed
        assert len(episodes) == 2

        episode1 = episodes[0]
        assert episode1.title == 'Episode 1'
        assert episode1.description == 'This is episode 1'
        assert episode1.pub_date == '2022-01-01'
        assert episode1.duration == '00:30:00'
        assert episode1.duration_in_seconds == 1800
        assert episode1.audio_url == 'audio_url'
        assert episode1.episode_number == '1'

        episode2 = episodes[1]
        assert episode2.title == 'Episode 2'
        assert episode2.description == 'This is episode 2'
        assert episode2.pub_date == '2022-01-02'
        assert episode2.duration == '00:45:00'
        assert episode2.duration_in_seconds == 2700
        assert episode2.audio_url == 'audio_url'
        assert episode2.episode_number == '2'


