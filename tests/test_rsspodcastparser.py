import pytest
from zpodcast.rsspodcastparser import RSSPodcastParser
from zpodcast.podcastdata import PodcastData
from zpodcast.podcastepisodelist import PodcastEpisodeList
from zpodcast.podcastepisode import PodcastEpisode

def test_get_episodes(mocker):
    mock_feedparser = mocker.patch('zpodcast.rsspodcastparser.feedparser.parse')
    mock_feedparser.return_value.entries = [
        {
            'title': 'Episode 1',
            'description': 'Description 1',
            'published': 'Mon, 11 Apr 2016 15:00:00 +0100',
            'itunes_duration': '1800',
            'enclosures': [{'href': 'https://example.com/episode1.mp3'}],
            'itunes_episode': 1
        },
        {
            'title': 'Episode 2',
            'description': 'Description 2',
            'published': 'Tue, 12 Apr 2016 15:00:00 +0100',
            'itunes_duration': '3600',
            'enclosures': [{'href': 'https://example.com/episode2.mp3'}],
            'itunes_episode': 2
        }
    ]

    episodes = RSSPodcastParser.get_episodes('https://example.com/feed.rss')

    assert len(episodes) == 2
    assert episodes[0].title == 'Episode 1'
    assert episodes[0].description == 'Description 1'
    assert episodes[0].pub_date.isoformat() == '2016-04-11T14:00:00+00:00'
    assert episodes[0].duration == 1800
    assert episodes[0].audio_url == 'https://example.com/episode1.mp3'
    assert episodes[0].episode_number == 1

    assert episodes[1].title == 'Episode 2'
    assert episodes[1].description == 'Description 2'
    assert episodes[1].pub_date.isoformat() == '2016-04-12T14:00:00+00:00'
    assert episodes[1].duration == 3600
    assert episodes[1].audio_url == 'https://example.com/episode2.mp3'
    assert episodes[1].episode_number == 2

def test_retrieve_and_add_episodes(mocker):
    mock_get_episodes = mocker.patch('zpodcast.rsspodcastparser.RSSPodcastParser.get_episodes')
    mock_get_episodes.return_value = [
        PodcastEpisode(
            title='Episode 1',
            description='Description 1',
            pub_date='Mon, 11 Apr 2016 15:00:00 +0100',
            duration=1800,
            audio_url='https://example.com/episode1.mp3',
            episode_number=1
        ),
        PodcastEpisode(
            title='Episode 2',
            description='Description 2',
            pub_date='Tue, 12 Apr 2016 15:00:00 +0100',
            duration=3600,
            audio_url='https://example.com/episode2.mp3',
            episode_number=2
        )
    ]

    podcast_data = PodcastData(
        title='Test Podcast',
        podcast_url='https://example.com/feed.rss',
        host='John Doe',
        description='Test Description',
        episodelists=[]
    )

    RSSPodcastParser.retrieve_and_add_episodes(podcast_data)

    assert len(podcast_data.episodelists) == 1
    assert podcast_data.episodelists[0].name == 'Test Podcast episode list'
    assert len(podcast_data.episodelists[0].episodes) == 2
    assert podcast_data.episodelists[0].episodes[0].title == 'Episode 1'
    assert podcast_data.episodelists[0].episodes[1].title == 'Episode 2'
