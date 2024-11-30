import pytest
from zpodcast.podcastdata import PodcastData
from zpodcast.podcastlist import PodcastList

def test_add_podcast():
    podcast = PodcastData(
        title="Test Podcast",
        podcast_url="http://example.com/podcast.rss",
        host="John Doe",
        description="This is a test podcast",
        episodelists=[],
        podcast_priority=5,
        image_url="http://example.com/image.jpg"
    )
    podcast_list = PodcastList([podcast])
    assert podcast_list.get_podcast(0) == podcast

def test_add_podcast_object():
    podcast = PodcastData(
        title="Test Podcast",
        podcast_url="http://example.com/podcast.rss",
        host="John Doe",
        description="This is a test podcast",
        episodelists=[],
        podcast_priority=5,
        image_url="http://example.com/image.jpg"
    )
    
    with pytest.raises(ValueError):
        podcast_list = PodcastList(podcast)
    
def test_add_podcast_object_int():
    podcast = PodcastData(
        title="Test Podcast",
        podcast_url="http://example.com/podcast.rss",
        host="John Doe",
        description="This is a test podcast",
        episodelists=[],
        podcast_priority=5,
        image_url="http://example.com/image.jpg"
    )
    
    with pytest.raises(ValueError):
        podcast_list = PodcastList(1)


def test_remove_podcast():
    podcast1 = PodcastData(
        title="Test Podcast 1",
        podcast_url="http://example.com/podcast1.rss",
        host="John Doe",
        description="This is a test podcast 1",
        episodelists=[],
        podcast_priority=5,
        image_url="http://example.com/image1.jpg"
    )
    podcast2 = PodcastData(
        title="Test Podcast 2",
        podcast_url="http://example.com/podcast2.rss",
        host="Jane Doe",
        description="This is a test podcast 2",
        episodelists=[],
        podcast_priority=5,
        image_url="http://example.com/image2.jpg"
    )
    podcast_list = PodcastList([podcast1, podcast2])
    assert len(podcast_list.podcasts) == 2
    podcast_list.remove_podcast(podcast1)
    assert len(podcast_list.podcasts) == 1
    assert podcast_list.podcasts[0] == podcast2

def test_get_all_podcasts():
    podcast1 = PodcastData(
        title="Test Podcast 1",
        podcast_url="http://example.com/podcast1.rss",
        host="John Doe",
        description="This is a test podcast 1",
        episodelists=[],
        podcast_priority=5,
        image_url="http://example.com/image1.jpg"
    )
    podcast2 = PodcastData(
        title="Test Podcast 2",
        podcast_url="http://example.com/podcast2.rss",
        host="Jane Doe",
        description="This is a test podcast 2",
        episodelists=[],
        podcast_priority=5,
        image_url="http://example.com/image2.jpg"
    )
    podcast_list = PodcastList([podcast1, podcast2])
    all_podcasts = podcast_list.podcasts
    assert len(all_podcasts) == 2
    assert all_podcasts[0] == podcast1
    assert all_podcasts[1] == podcast2

def test_get_podcast():
    podcast1 = PodcastData(
        title="Test Podcast 1",
        podcast_url="http://example.com/podcast1.rss",
        host="John Doe",
        description="This is a test podcast 1",
        episodelists=[],
        podcast_priority=5,
        image_url="http://example.com/image1.jpg"
    )
    podcast2 = PodcastData(
        title="Test Podcast 2",
        podcast_url="http://example.com/podcast2.rss",
        host="Jane Doe",
        description="This is a test podcast 2",
        episodelists=[],
        podcast_priority=5,
        image_url="http://example.com/image2.jpg"
    )
    podcast_list = PodcastList([podcast1, podcast2])
    
    podcast = podcast_list.get_podcast(0)
    assert podcast == podcast1

    with pytest.raises(ValueError):
        podcast = podcast_list.get_podcast(-1)

    with pytest.raises(ValueError):
        podcast = podcast_list.get_podcast(2)

    with pytest.raises(ValueError):
        podcast = podcast_list.get_podcast("invalid")

def test_podcastlist_to_dict():
    podcast1 = PodcastData(
        title="Test Podcast 1",
        podcast_url="http://example.com/podcast1.rss",
        host="John Doe",
        description="This is a test podcast 1",
        episodelists=[],
        podcast_priority=5,
        image_url="http://example.com/image1.jpg"
    )
    podcast2 = PodcastData(
        title="Test Podcast 2",
        podcast_url="http://example.com/podcast2.rss",
        host="Jane Doe",
        description="This is a test podcast 2",
        episodelists=[],
        podcast_priority=5,
        image_url="http://example.com/image2.jpg"
    )
    podcast_list = PodcastList([podcast1, podcast2])
    podcast_list_dict = podcast_list.to_dict()
    assert podcast_list_dict == {
        "podcasts": [
            {
                "title": "Test Podcast 1",
                "podcast_url": "http://example.com/podcast1.rss",
                "host": "John Doe",
                "description": "This is a test podcast 1",
                "episodes": [],
                "podcast_priority": 5,
                "image_url": "http://example.com/image1.jpg"
            },
            {
                "title": "Test Podcast 2",
                "podcast_url": "http://example.com/podcast2.rss",
                "host": "Jane Doe",
                "description": "This is a test podcast 2",
                "episodes": [],
                "podcast_priority": 5,
                "image_url": "http://example.com/image2.jpg"
            }
        ]
    }

def test_podcastlist_from_dict():
    podcast_list_dict = {
        "podcasts": [
            {
                "title": "Test Podcast 1",
                "podcast_url": "http://example.com/podcast1.rss",
                "host": "John Doe",
                "description": "This is a test podcast 1",
                "episodes": [],
                "podcast_priority": 5,
                "image_url": "http://example.com/image1.jpg"
            },
            {
                "title": "Test Podcast 2",
                "podcast_url": "http://example.com/podcast2.rss",
                "host": "Jane Doe",
                "description": "This is a test podcast 2",
                "episodes": [],
                "podcast_priority": 5,
                "image_url": "http://example.com/image2.jpg"
            }
        ]
    }
    podcast_list = PodcastList.from_dict(podcast_list_dict)
    assert len(podcast_list.podcasts) == 2
    assert podcast_list.podcasts[0].title == "Test Podcast 1"
    assert podcast_list.podcasts[1].title == "Test Podcast 2"
