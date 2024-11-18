import pytest
from zpodcast.podcastlist import PodcastList
from zpodcast.podcastdata import PodcastData

def test_add_podcast():
    podcast_list = PodcastList()
    podcast = PodcastData(
        title="Test Podcast",
        podcast_url="http://example.com/podcast.rss",
        host="John Doe",
        description="This is a test podcast",
        episodes=[],
        podcast_priority=5,
        image_url="http://example.com/image.jpg"
    )
    podcast_list.add_podcast(podcast)
    assert len(podcast_list.get_all_podcasts()) == 1
    assert podcast_list.get_all_podcasts()[0] == podcast

def test_remove_podcast():
    podcast_list = PodcastList()
    podcast1 = PodcastData(
        title="Test Podcast 1",
        podcast_url="http://example.com/podcast1.rss",
        host="John Doe",
        description="This is a test podcast 1",
        episodes=[],
        podcast_priority=5,
        image_url="http://example.com/image1.jpg"
    )
    podcast2 = PodcastData(
        title="Test Podcast 2",
        podcast_url="http://example.com/podcast2.rss",
        host="Jane Doe",
        description="This is a test podcast 2",
        episodes=[],
        podcast_priority=5,
        image_url="http://example.com/image2.jpg"
    )
    podcast_list.add_podcast(podcast1)
    podcast_list.add_podcast(podcast2)
    podcast_list.remove_podcast(podcast1)
    assert len(podcast_list.get_all_podcasts()) == 1
    assert podcast_list.get_all_podcasts()[0] == podcast2

def test_insert_podcast():
    podcast_list = PodcastList()
    podcast1 = PodcastData(
        title="Test Podcast 1",
        podcast_url="http://example.com/podcast1.rss",
        host="John Doe",
        description="This is a test podcast 1",
        episodes=[],
        podcast_priority=5,
        image_url="http://example.com/image1.jpg"
    )
    podcast2 = PodcastData(
        title="Test Podcast 2",
        podcast_url="http://example.com/podcast2.rss",
        host="Jane Doe",
        description="This is a test podcast 2",
        episodes=[],
        podcast_priority=5,
        image_url="http://example.com/image2.jpg"
    )
    podcast_list.add_podcast(podcast1)
    podcast_list.insert_podcast(0, podcast2)
    assert len(podcast_list.get_all_podcasts()) == 2
    assert podcast_list.get_all_podcasts()[0] == podcast2
    assert podcast_list.get_all_podcasts()[1] == podcast1

def test_get_all_podcasts():
    podcast_list = PodcastList()
    podcast1 = PodcastData(
        title="Test Podcast 1",
        podcast_url="http://example.com/podcast1.rss",
        host="John Doe",
        description="This is a test podcast 1",
        episodes=[],
        podcast_priority=5,
        image_url="http://example.com/image1.jpg"
    )
    podcast2 = PodcastData(
        title="Test Podcast 2",
        podcast_url="http://example.com/podcast2.rss",
        host="Jane Doe",
        description="This is a test podcast 2",
        episodes=[],
        podcast_priority=5,
        image_url="http://example.com/image2.jpg"
    )
    podcast_list.add_podcast(podcast1)
    podcast_list.add_podcast(podcast2)
    all_podcasts = podcast_list.get_all_podcasts()
    assert len(all_podcasts) == 2
    assert all_podcasts[0] == podcast1
    assert all_podcasts[1] == podcast2

def test_get_podcast():
    podcast_list = PodcastList()
    podcast1 = PodcastData(
        title="Test Podcast 1",
        podcast_url="http://example.com/podcast1.rss",
        host="John Doe",
        description="This is a test podcast 1",
        episodes=[],
        podcast_priority=5,
        image_url="http://example.com/image1.jpg"
    )
    podcast2 = PodcastData(
        title="Test Podcast 2",
        podcast_url="http://example.com/podcast2.rss",
        host="Jane Doe",
        description="This is a test podcast 2",
        episodes=[],
        podcast_priority=5,
        image_url="http://example.com/image2.jpg"
    )
    podcast_list.add_podcast(podcast1)
    podcast_list.add_podcast(podcast2)
    retrieved_podcast = podcast_list.get_podcast(1)
    assert retrieved_podcast == podcast2

    with pytest.raises(ValueError):
        podcast_list.get_podcast(-1)

    with pytest.raises(ValueError):
        podcast_list.get_podcast(2)

    with pytest.raises(ValueError):
        podcast_list.get_podcast("invalid")
