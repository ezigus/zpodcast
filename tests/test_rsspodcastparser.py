import pytest
from zpodcast.rsspodcastparser import RSSPodcastParser
from zpodcast.podcastdata import PodcastData
from zpodcast.podcastepisodelist import PodcastEpisodeList
from zpodcast.podcastepisode import PodcastEpisode

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
def mock_feedparser(mocker):
    mock_feedparser = mocker.patch('zpodcast.rsspodcastparser.feedparser.parse')
    mock_feedparser.return_value.entries = 
    {
        'title': podcast_data.title,
        'description': podcast_data.description,
        'link': podcast_data.podcast_url,
        'author': podcast_data.host,
        'item' :
            {
                'title': podcast_episode1_title,
                'description': podcast_episode1_description,
                'published': podcast_episode1_published,
                'itunes_duration': podcast_episode1_published,
                'enclosures': podcast_episode1_enclosures,
                'itunes_episode': podcast_episode1_episode
            },
        'item' :
            {
                'title': podcast_episode1_title,
                'description': podcast_episode1_description,
                'published': podcast_episode1_published,
                'itunes_duration': podcast_episode1_published,
                'enclosures': podcast_episode1_enclosures,
                'itunes_episode': podcast_episode1_episode
            }
    }

def test_get_episodes(mock_feedparser):

    episodes = RSSPodcastParser.get_episodes('https://example.com/feed.rss')

    assert len(episodes) == 2
    assert episodes[0].title == podcast_episode1_title
    assert episodes[0].description == podcast_episode1_description
    assert episodes[0].pub_date.isoformat() == podcast_episode1_published
    assert episodes[0].duration == podcast_episode1_duration
    assert episodes[0].audio_url == podcast_episode1_enclosures
    assert episodes[0].episode_number == podcast_episode1_episode

    assert episodes[1].title == podcast_episode2_title
    assert episodes[1].description == podcast_episode2_description
    assert episodes[1].pub_date.isoformat() == podcast_episode2_published
    assert episodes[1].duration == podcast_episode2_duration
    assert episodes[1].audio_url == podcast_episode2_enclosures
    assert episodes[1].episode_number == podcast_episode2_episode

def test_get_rss_metadata(mock_feedparser):
    podcast_meta = RSSPodcastParser.get_rss_metadata('https://example.com/feed.rss')

    assert podcast_meta['title'] == podcast_data.title
    assert podcast_meta['description'] == podcast_data.description
    assert podcast_meta['author'] == podcast_data.host
    assert podcast_meta['image'] == None