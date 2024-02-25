import unittest
from unittest.mock import patch
from rsspodcastparser import RSSPodcastParser
from podcastepisode import PodcastEpisode

class TestRSSPodcastParser(unittest.TestCase):
    def test_get_episodes(self):
        # Mock the feedparser library
        with patch('rsspodcastparser.feedparser') as mock_feedparser:
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
            self.assertEqual(len(episodes), 2)

            episode1 = episodes[0]
            self.assertEqual(episode1.title, 'Episode 1')
            self.assertEqual(episode1.description, 'This is episode 1')
            self.assertEqual(episode1.pub_date, '2022-01-01')
            self.assertEqual(episode1.duration, '00:30:00')
            self.assertEqual(episode1.duration_in_seconds, 1800)
            self.assertEqual(episode1.audio_url, 'audio_url')
            self.assertEqual(episode1.episode_number, '1')

            episode2 = episodes[1]
            self.assertEqual(episode2.title, 'Episode 2')
            self.assertEqual(episode2.description, 'This is episode 2')
            self.assertEqual(episode2.pub_date, '2022-01-02')
            self.assertEqual(episode2.duration, '00:45:00')
            self.assertEqual(episode2.duration_in_seconds, 2700)
            self.assertEqual(episode2.audio_url, 'audio_url')
            self.assertEqual(episode2.episode_number, '2')

    def test_convert_duration_to_seconds(self):
        # Test case for duration in seconds
        duration = '3600'
        seconds = RSSPodcastParser._convert_duration_to_seconds(duration)
        self.assertEqual(seconds, 3600)

        # Test case for duration in HH:MM:SS format
        duration = '01:30:00'
        seconds = RSSPodcastParser._convert_duration_to_seconds(duration)
        self.assertEqual(seconds, 5400)

        # Test case for duration in MM:SS format
        duration = '45:30'
        seconds = RSSPodcastParser._convert_duration_to_seconds(duration)
        self.assertEqual(seconds, 2730)

        # Test case for None duration
        duration = None
        seconds = RSSPodcastParser._convert_duration_to_seconds(duration)
        self.assertIsNone(seconds)

if __name__ == '__main__':
    unittest.main()
