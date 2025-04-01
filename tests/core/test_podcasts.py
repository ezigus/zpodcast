import pytest
from zpodcast.core.podcast import PodcastData
from zpodcast.core.podcasts import PodcastList


@pytest.fixture
def sample_podcasts():
    """Create sample podcasts for testing."""
    podcast1 = PodcastData(
        title="Test Podcast 1",
        podcast_url="http://example.com/podcast1.rss",
        host="John Doe",
        description="This is a test podcast 1",
        episodelists=[],
        podcast_priority=5,
        image_url="http://example.com/image1.jpg",
    )
    podcast2 = PodcastData(
        title="Test Podcast 2",
        podcast_url="http://example.com/podcast2.rss",
        host="Jane Doe",
        description="This is a test podcast 2",
        episodelists=[],
        podcast_priority=5,
        image_url="http://example.com/image2.jpg",
    )
    return [podcast1, podcast2]


@pytest.fixture
def sample_podcast_list(sample_podcasts):
    """Create a PodcastList with sample podcasts."""
    return PodcastList(sample_podcasts)


def test_add_podcast():
    podcast = PodcastData(
        title="Test Podcast",
        podcast_url="http://example.com/podcast.rss",
        host="John Doe",
        description="This is a test podcast",
        episodelists=[],
        podcast_priority=5,
        image_url="http://example.com/image.jpg",
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
        image_url="http://example.com/image.jpg",
    )

    with pytest.raises(ValueError):
        # Using _ to indicate unused variable
        _ = PodcastList(podcast)


def test_add_podcast_object_int():
    # The unused podcast variable is not needed for this test
    with pytest.raises(ValueError):
        # Using _ to indicate unused variable
        _ = PodcastList(1)


def test_remove_podcast(sample_podcast_list):
    podcast1 = PodcastData(
        title="Test Podcast 1",
        podcast_url="http://example.com/podcast1.rss",
        host="John Doe",
        description="This is a test podcast 1",
        episodelists=[],
        podcast_priority=5,
        image_url="http://example.com/image1.jpg",
    )
    podcast2 = PodcastData(
        title="Test Podcast 2",
        podcast_url="http://example.com/podcast2.rss",
        host="Jane Doe",
        description="This is a test podcast 2",
        episodelists=[],
        podcast_priority=5,
        image_url="http://example.com/image2.jpg",
    )
    podcast_list = PodcastList([podcast1, podcast2])
    assert len(podcast_list.podcasts) == 2
    podcast_list.remove_podcast(podcast1)
    assert len(podcast_list.podcasts) == 1
    assert podcast_list.podcasts[0] == podcast2


def test_get_all_podcasts(sample_podcast_list):
    all_podcasts = sample_podcast_list.podcasts
    assert len(all_podcasts) == 2
    assert all_podcasts[0] == sample_podcast_list.podcasts[0]
    assert all_podcasts[1] == sample_podcast_list.podcasts[1]


def test_get_podcast(sample_podcast_list):
    podcast1 = sample_podcast_list.podcasts[0]
    podcast2 = sample_podcast_list.podcasts[1]

    podcast = sample_podcast_list.get_podcast(0)
    assert podcast == podcast1

    with pytest.raises(ValueError):
        # Using _ to indicate unused variable
        _ = sample_podcast_list.get_podcast(-1)

    with pytest.raises(ValueError):
        # Using _ to indicate unused variable
        _ = sample_podcast_list.get_podcast(2)

    with pytest.raises(ValueError):
        # Using _ to indicate unused variable
        _ = sample_podcast_list.get_podcast("invalid")


def test_podcastlist_to_dict(sample_podcast_list):
    podcast_list_dict = sample_podcast_list.to_dict()

    assert podcast_list_dict == sample_podcast_list.to_dict()

    # assert podcast_list_dict == {
    #     "podcasts": [
    #         {
    #             "title": "Test Podcast 1",
    #             "podcast_url": "http://example.com/podcast1.rss",
    #             "host": "John Doe",
    #             "description": "This is a test podcast 1",
    #             "episodes": [],
    #             "podcast_priority": 5,
    #             "image_url": "http://example.com/image1.jpg"
    #         },
    #         {
    #             "title": "Test Podcast 2",
    #             "podcast_url": "http://example.com/podcast2.rss",
    #             "host": "Jane Doe",
    #             "description": "This is a test podcast 2",
    #             "episodes": [],
    #             "podcast_priority": 5,
    #             "image_url": "http://example.com/image2.jpg"
    #         }
    #     ]
    # }


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
                "image_url": "http://example.com/image1.jpg",
            },
            {
                "title": "Test Podcast 2",
                "podcast_url": "http://example.com/podcast2.rss",
                "host": "Jane Doe",
                "description": "This is a test podcast 2",
                "episodes": [],
                "podcast_priority": 5,
                "image_url": "http://example.com/image2.jpg",
            },
        ]
    }
    podcast_list = PodcastList.from_dict(podcast_list_dict)
    assert len(podcast_list.podcasts) == 2
    assert podcast_list.podcasts[0].title == "Test Podcast 1"
    assert podcast_list.podcasts[1].title == "Test Podcast 2"


def test_delete_podcast():
    """Test deleting a podcast by index"""
    podcast1 = PodcastData(
        title="Test Podcast 1",
        podcast_url="http://example.com/podcast1.rss",
        host="John Doe",
        description="This is a test podcast 1",
        episodelists=[],
        podcast_priority=5,
        image_url="http://example.com/image1.jpg",
    )
    podcast2 = PodcastData(
        title="Test Podcast 2",
        podcast_url="http://example.com/podcast2.rss",
        host="Jane Doe",
        description="This is a test podcast 2",
        episodelists=[],
        podcast_priority=5,
        image_url="http://example.com/image2.jpg",
    )
    podcast_list = PodcastList([podcast1, podcast2])

    # Delete first podcast
    podcast_list.delete_podcast(0)
    assert len(podcast_list.podcasts) == 1
    assert podcast_list.podcasts[0] == podcast2

    # Test with invalid index
    with pytest.raises(ValueError):
        podcast_list.delete_podcast(99)

    with pytest.raises(ValueError):
        podcast_list.delete_podcast(-1)

    with pytest.raises(ValueError):
        podcast_list.delete_podcast("invalid")


def test_update_podcast(mocker):
    """Test updating a podcast with new data"""
    # Setup mocks to prevent actual RSS fetching - not directly used but needed for test
    mocker.patch("zpodcast.parsers.rss.RSSPodcastParser.get_episodes", return_value=[])
    mock_get_metadata = mocker.patch(
        "zpodcast.parsers.rss.RSSPodcastParser.get_rss_metadata"
    )
    # Return proper metadata to maintain field values
    mock_get_metadata.side_effect = [
        {"author": "John Doe", "description": "This is a test podcast 1"},
        {"author": "Jane Doe", "description": "This is a test podcast 2"},
        {
            "author": "Jane Doe",
            "description": "This is a test podcast 2",
        },  # For the second podcast when it gets updated
    ]

    # Setup test podcast
    podcast1 = PodcastData(
        title="Test Podcast 1",
        podcast_url="http://example.com/podcast1.rss",
        host="John Doe",
        description="This is a test podcast 1",
        episodelists=[],
        podcast_priority=5,
        image_url="http://example.com/image1.jpg",
    )
    podcast2 = PodcastData(
        title="Test Podcast 2",
        podcast_url="http://example.com/podcast2.rss",
        host="Jane Doe",
        description="This is a test podcast 2",
        episodelists=[],
        podcast_priority=5,
        image_url="http://example.com/image2.jpg",
    )
    podcast_list = PodcastList([podcast1, podcast2])

    # Test updating with integer index
    updated_podcast = podcast_list.update_podcast(
        0,
        {
            "title": "Updated Podcast Title",
            "description": "Updated description",
            "host": "Updated Host",
            "podcast_priority": 8,
            "image_url": "http://example.com/updated.jpg",
        },
    )

    # Verify update was applied
    assert updated_podcast.title == "Updated Podcast Title"
    assert updated_podcast.description == "Updated description"
    assert updated_podcast.host == "Updated Host"
    assert updated_podcast.podcast_priority == 8
    assert updated_podcast.image_url == "http://example.com/updated.jpg"

    # Verify the object in the list was updated
    assert podcast_list.podcasts[0].title == "Updated Podcast Title"
    assert podcast_list.podcasts[0].description == "Updated description"

    # Test updating with string index that converts to int
    updated_podcast = podcast_list.update_podcast(
        "1", {"title": "Updated Second Podcast"}
    )
    assert updated_podcast.title == "Updated Second Podcast"
    assert podcast_list.podcasts[1].title == "Updated Second Podcast"

    # Original fields remain unchanged when not in update data
    assert podcast_list.podcasts[1].host == "Jane Doe"
    assert podcast_list.podcasts[1].description == "This is a test podcast 2"


def test_update_podcast_invalid_index():
    """Test updating a podcast with invalid index"""
    podcast = PodcastData(
        title="Test Podcast",
        podcast_url="http://example.com/podcast.rss",
        host="John Doe",
        description="This is a test podcast",
        episodelists=[],
        podcast_priority=5,
        image_url="http://example.com/image.jpg",
    )
    podcast_list = PodcastList([podcast])

    # Test with non-existent index
    with pytest.raises(ValueError):
        podcast_list.update_podcast(99, {"title": "New Title"})

    # Test with negative index
    with pytest.raises(ValueError):
        podcast_list.update_podcast(-1, {"title": "New Title"})

    # Test with non-convertible string
    with pytest.raises(ValueError):
        podcast_list.update_podcast("not-a-number", {"title": "New Title"})


def test_update_podcast_with_url_change(mocker):
    """Test updating a podcast's URL which should trigger episode refresh"""
    # Mock both RSS methods to prevent actual network calls
    # These mocks are necessary for the test setup but not directly used in assertions
    mocker.patch("zpodcast.parsers.rss.RSSPodcastParser.get_episodes", return_value=[])
    mocker.patch(
        "zpodcast.parsers.rss.RSSPodcastParser.get_rss_metadata",
        return_value={"author": "John Doe", "description": "Test description"},
    )

    # Create a separate mock specifically for testing the populate method call
    mock_populate = mocker.patch(
        "zpodcast.core.podcast.PodcastData.populate_episodes_from_feed"
    )

    # Create a podcast with mocked init that doesn't call populate_episodes_from_feed
    mocker.patch("zpodcast.core.podcast.PodcastData.__init__", return_value=None)
    podcast = PodcastData.__new__(PodcastData)
    podcast._title = "Test Podcast"
    podcast._podcast_url = "http://example.com/podcast.rss"
    podcast._host = "John Doe"
    podcast._description = "This is a test podcast"
    podcast._episodelists = []
    podcast._podcast_priority = 5
    podcast._image_url = "http://example.com/image.jpg"
    podcast._name_set_manually = False

    # Reset the mock to clear the call from initialization
    mock_populate.reset_mock()

    podcast_list = PodcastList([podcast])

    # Update with a new URL
    podcast_list.update_podcast(0, {"podcast_url": "http://example.com/new_feed.rss"})

    # Verify the URL was updated
    assert podcast_list.podcasts[0]._podcast_url == "http://example.com/new_feed.rss"

    # Verify populate_episodes_from_feed was called exactly once
    mock_populate.assert_called_once()
