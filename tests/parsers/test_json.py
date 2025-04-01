import pytest
from unittest.mock import patch, mock_open
from zpodcast.parsers.json import PodcastJSON
from zpodcast.core.podcasts import PodcastList
from zpodcast.core.playlists import PodcastPlaylist
from zpodcast.core.podcast import PodcastData
from zpodcast.core.playlist import PodcastEpisodeList
from zpodcast.core.episode import PodcastEpisode


@pytest.fixture
def sample_podcast_list():
    podcastepisodelist = PodcastEpisodeList(
        name="Test podcast Episode List",
        episodes=[
            PodcastEpisode(
                title="Episode 1", audio_url="https://example.com/episode1.mp3"
            ),
            PodcastEpisode(
                title="Episode 2", audio_url="https://example.com/episode2.mp3"
            ),
        ],
    )

    podcast1 = PodcastData(
        title="Test Podcast 1",
        podcast_url="http://example.com/podcast1.rss",
        host="John Doe",
        description="This is a test podcast 1",
        episodelists=[podcastepisodelist],
        podcast_priority=5,
        image_url="http://example.com/image1.jpg",
    )
    podcast2 = PodcastData(
        title="Test Podcast 2",
        podcast_url="http://example.com/podcast2.rss",
        host="Jane Doe",
        description="This is a test podcast 2",
        episodelists=[podcastepisodelist],
        podcast_priority=5,
        image_url="http://example.com/image2.jpg",
    )
    return PodcastList([podcast1, podcast2])


@pytest.fixture
def sample_playlist():
    episodes1 = PodcastEpisodeList(
        name="Test playList 1",
        episodes=[
            PodcastEpisode(
                title="Episode 1", audio_url="https://example.com/episode1.mp3"
            ),
            PodcastEpisode(
                title="Episode 2", audio_url="https://example.com/episode2.mp3"
            ),
        ],
    )

    episodes2 = PodcastEpisodeList(
        name="Test playList 2",
        episodes=[
            PodcastEpisode(
                title="Episode 3", audio_url="https://example.com/episode3.mp3"
            ),
            PodcastEpisode(
                title="Episode 4", audio_url="https://example.com/episode4.mp3"
            ),
        ],
    )
    return PodcastPlaylist([episodes1, episodes2])


@patch("zpodcast.parsers.json.open", new_callable=mock_open)
@patch("json.dump")
def test_export_podcast_list_mock(mock_json_dump, mock_file, sample_podcast_list):
    filename = "test_podcast_list.json"

    PodcastJSON.export_podcast_list(sample_podcast_list, filename)

    # Check that the file was opened for writing
    mock_file.assert_called_once_with(filename, "w")

    # Check that json.dump was called with the correct arguments
    mock_json_dump.assert_called_once()
    args, _ = mock_json_dump.call_args
    assert args[0]["version"] == "0.1"
    assert "podcastlist" in args[0]
    assert args[0]["podcastlist"] == sample_podcast_list.to_dict()


@patch("zpodcast.parsers.json.open", new_callable=mock_open)
@patch("json.load")
def test_import_podcast_list_mock(mock_json_load, mock_file, sample_podcast_list):
    filename = "test_podcast_list.json"

    # Configure mock to return sample podcast list data
    mock_data = {"version": "0.1", "podcastlist": sample_podcast_list.to_dict()}
    mock_json_load.return_value = mock_data

    # Call the function under test
    imported_podcast_list = PodcastJSON.import_podcast_list(filename)

    # Verify the file was opened for reading
    mock_file.assert_called_once_with(filename, "r")

    # Verify the result
    assert imported_podcast_list.to_dict() == sample_podcast_list.to_dict()


@patch("zpodcast.parsers.json.open", new_callable=mock_open)
@patch("json.dump")
def test_export_podcast_playlist_mock(mock_json_dump, mock_file, sample_playlist):
    filename = "test_podcast_playlist.json"

    PodcastJSON.export_podcast_playlist(sample_playlist, filename)

    # Check that the file was opened for writing
    mock_file.assert_called_once_with(filename, "w")

    # Check that json.dump was called with the correct arguments
    mock_json_dump.assert_called_once()
    args, _ = mock_json_dump.call_args
    assert args[0]["version"] == "0.1"
    assert "podcastplaylist" in args[0]
    assert args[0]["podcastplaylist"] == sample_playlist.to_dict()


@patch("zpodcast.parsers.json.open", new_callable=mock_open)
@patch("json.load")
def test_import_podcast_playlist_mock(mock_json_load, mock_file, sample_playlist):
    filename = "test_podcast_playlist.json"

    # Configure mock to return sample playlist data
    mock_data = {"version": "0.1", "podcastplaylist": sample_playlist.to_dict()}
    mock_json_load.return_value = mock_data

    # Call the function under test
    imported_playlist = PodcastJSON.import_podcast_playlist(filename)

    # Verify the file was opened for reading
    mock_file.assert_called_once_with(filename, "r")

    # Verify the result
    assert imported_playlist.to_dict() == sample_playlist.to_dict()


def test_unsupported_version_podcast_list():
    with patch("zpodcast.parsers.json.open", new_callable=mock_open), patch(
        "json.load", side_effect=[{"version": "0.2", "podcastlist": {}}]
    ):
        with pytest.raises(ValueError, match="Unsupported version"):
            PodcastJSON.import_podcast_list("test.json")


def test_unsupported_version_podcast_playlist():
    with patch("zpodcast.parsers.json.open", new_callable=mock_open), patch(
        "json.load", side_effect=[{"version": "0.2", "podcastplaylist": {}}]
    ):
        with pytest.raises(ValueError, match="Unsupported version"):
            PodcastJSON.import_podcast_playlist("test.json")


def test_default_filename_podcast_list(sample_podcast_list):
    with patch("zpodcast.parsers.json.open", new_callable=mock_open) as mock_file:
        PodcastJSON.export_podcast_list(sample_podcast_list)

        # Check that the default filename was used
        mock_file.assert_called_once_with(
            f"PodcastList-{PodcastJSON.VERSION}.json", "w"
        )


def test_default_filename_podcast_playlist(sample_playlist):
    with patch("zpodcast.parsers.json.open", new_callable=mock_open) as mock_file:
        PodcastJSON.export_podcast_playlist(sample_playlist)

        # Check that the default filename was used
        mock_file.assert_called_once_with(
            f"PodcastPlaylist-{PodcastJSON.VERSION}.json", "w"
        )
