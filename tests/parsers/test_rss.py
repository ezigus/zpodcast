import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from zpodcast.parsers.rss import RSSPodcastParser
from zpodcast.core.podcast import PodcastData
from zpodcast.core.playlist import PodcastEpisodeList
from zpodcast.core.episode import PodcastEpisode

podcast_data = PodcastData(
    title='Test Podcast',
    podcast_url='https://example.com/feed.rss',
    host='John Doe',
    description='Test Description',
    episodelists=[]
)

podcast_episode1_title = 'Episode 1'
podcast_episode1_description =  'Description 1'
podcast_episode1_published =  'Mon, 11 Apr 2016 15:00:00 +0100'
podcast_episode1_duration =  '1800'
podcast_episode1_enclosures = [{'href': 'https://example.com/episode1.mp3'}]
podcast_episode1_episode = 1

podcast_episode2_title = 'Episode 2'
podcast_episode2_description =  'Description 2'
podcast_episode2_published =  'Mon, 12 Apr 2016 15:00:00 +0100'
podcast_episode2_duration =  '1800'
podcast_episode2_enclosures = [{'href': 'https://example.com/episode1.mp3'}]
podcast_episode2_episode = 2

@pytest.fixture
def mock_feedparser():
    with patch('feedparser.parse') as mock_parse:
        yield mock_parse

def test_get_episodes_success(mock_feedparser):
    # Mock feed data
    mock_feed = MagicMock()
    mock_feed.bozo = False
    mock_feed.entries = [
        {
            'title': 'Test Episode 1',
            'enclosures': [{'href': 'https://example.com/episode1.mp3'}],
            'description': 'Test Description 1',
            'published': 'Mon, 11 Apr 2024 15:00:00 +0100',
            'itunes_duration': '1800',
            'itunes_episode': 1,
            'image': {'href': 'https://example.com/episode1.jpg'},
            'guid': 'episode1-guid'
        },
        {
            'title': 'Test Episode 2',
            'enclosures': [{'href': 'https://example.com/episode2.mp3'}],
            'description': 'Test Description 2',
            'published': 'Mon, 12 Apr 2024 15:00:00 +0100',
            'itunes_duration': '01:30:00',
            'itunes_episode': 2,
            'image': {'href': 'https://example.com/episode2.jpg'},
            'guid': 'episode2-guid'
        }
    ]
    mock_feedparser.return_value = mock_feed

    # Test getting episodes
    episodes = RSSPodcastParser.get_episodes('https://example.com/feed.rss')
    
    assert len(episodes) == 2
    assert isinstance(episodes[0], PodcastEpisode)
    assert episodes[0].title == 'Test Episode 1'
    assert episodes[0].audio_url == 'https://example.com/episode1.mp3'
    assert episodes[0].duration == 1800  # 30 minutes in seconds
    assert episodes[1].duration == 5400  # 1:30:00 in seconds

def test_get_episodes_with_different_duration_formats(mock_feedparser):
    # Mock feed data with different duration formats
    mock_feed = MagicMock()
    mock_feed.bozo = False
    mock_feed.entries = [
        {
            'title': 'Episode 1',
            'enclosures': [{'href': 'https://example.com/episode1.mp3'}],
            'description': 'Description 1',
            'published': 'Mon, 11 Apr 2024 15:00:00 +0100',
            'itunes_duration': '45:30',  # MM:SS format
            'itunes_episode': 1
        },
        {
            'title': 'Episode 2',
            'enclosures': [{'href': 'https://example.com/episode2.mp3'}],
            'description': 'Description 2',
            'published': 'Mon, 12 Apr 2024 15:00:00 +0100',
            'itunes_duration': '3600',  # Seconds format
            'itunes_episode': 2
        }
    ]
    mock_feedparser.return_value = mock_feed

    episodes = RSSPodcastParser.get_episodes('https://example.com/feed.rss')
    
    assert len(episodes) == 2
    assert episodes[0].duration == 2730  # 45:30 in seconds
    assert episodes[1].duration == 3600  # 3600 seconds

def test_get_episodes_with_feed_error(mock_feedparser):
    # Mock feed with parsing error
    mock_feed = MagicMock()
    mock_feed.bozo = True
    mock_feed.bozo_exception = "Invalid XML"
    mock_feedparser.return_value = mock_feed

    episodes = RSSPodcastParser.get_episodes('https://example.com/invalid-feed.rss')
    assert len(episodes) == 0

def test_get_episodes_with_entry_error(mock_feedparser):
    # Mock feed with invalid entry
    mock_feed = MagicMock()
    mock_feed.bozo = False
    mock_feed.entries = [
        {
            'title': 'Valid Episode',
            'enclosures': [{'href': 'https://example.com/episode1.mp3'}],
            'description': 'Description',
            'published': 'Mon, 11 Apr 2024 15:00:00 +0100',
            'itunes_duration': '1800',
            'itunes_episode': 1
        },
        {
            'title': 'Invalid Episode',
            # Missing required fields
            'description': 'Description'
        }
    ]
    mock_feedparser.return_value = mock_feed

    episodes = RSSPodcastParser.get_episodes('https://example.com/feed.rss')
    assert len(episodes) == 1
    assert episodes[0].title == 'Valid Episode'

def test_get_rss_metadata_success(mock_feedparser):
    # Mock feed data
    mock_feed = MagicMock()
    mock_feed.bozo = False
    mock_feed.feed = {
        'title': 'Test Podcast',
        'description': 'Test Description',
        'author': 'Test Author',
        'image': {'href': 'https://example.com/podcast.jpg'}
    }
    mock_feedparser.return_value = mock_feed

    metadata = RSSPodcastParser.get_rss_metadata('https://example.com/feed.rss')
    
    assert metadata['title'] == 'Test Podcast'
    assert metadata['description'] == 'Test Description'
    assert metadata['author'] == 'Test Author'
    assert metadata['image'] == 'https://example.com/podcast.jpg'

def test_get_rss_metadata_with_feed_error(mock_feedparser):
    # Mock feed with parsing error
    mock_feed = MagicMock()
    mock_feed.bozo = True
    mock_feed.bozo_exception = "Invalid XML"
    mock_feedparser.return_value = mock_feed

    metadata = RSSPodcastParser.get_rss_metadata('https://example.com/invalid-feed.rss')
    assert metadata == {}