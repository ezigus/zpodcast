import pytest
from zpodcast.utils.sort import SortParameters


def test_sort_parameters_initialization():
    params = SortParameters(
        _episode_title=None,
        _episode_duration=None,
        _episode_date=None,
        _episode_rating=None,
        _podcast_title=None,
        _podcast_author=None
    )
    assert params.episode_title is None
    assert params.episode_duration is None
    assert params.episode_date is None
    assert params.episode_rating is None
    assert params.podcast_title is None
    assert params.podcast_author is None


def test_episode_title_setter():
    params = SortParameters(
        _episode_title=None,
        _episode_duration=None,
        _episode_date=None,
        _episode_rating=None,
        _podcast_title=None,
        _podcast_author=None
    )
    
    # Test valid values
    params.episode_title = "A-Z"
    assert params.episode_title == "A-Z"
    params.episode_title = "Z-A"
    assert params.episode_title == "Z-A"
    params.episode_title = None
    assert params.episode_title is None
    
    # Test invalid value
    with pytest.raises(ValueError):
        params.episode_title = "invalid"


def test_episode_duration_setter():
    params = SortParameters(
        _episode_title=None,
        _episode_duration=None,
        _episode_date=None,
        _episode_rating=None,
        _podcast_title=None,
        _podcast_author=None
    )
    
    # Test valid values
    params.episode_duration = "ShortToLong"
    assert params.episode_duration == "ShortToLong"
    params.episode_duration = "LongToShort"
    assert params.episode_duration == "LongToShort"
    params.episode_duration = None
    assert params.episode_duration is None
    
    # Test invalid value
    with pytest.raises(ValueError):
        params.episode_duration = "invalid"


def test_episode_date_setter():
    params = SortParameters(
        _episode_title=None,
        _episode_duration=None,
        _episode_date=None,
        _episode_rating=None,
        _podcast_title=None,
        _podcast_author=None
    )
    
    # Test valid values
    params.episode_date = "Earliest"
    assert params.episode_date == "Earliest"
    params.episode_date = "Latest"
    assert params.episode_date == "Latest"
    params.episode_date = None
    assert params.episode_date is None
    
    # Test invalid value
    with pytest.raises(ValueError):
        params.episode_date = "invalid"


def test_episode_rating_setter():
    params = SortParameters(
        _episode_title=None,
        _episode_duration=None,
        _episode_date=None,
        _episode_rating=None,
        _podcast_title=None,
        _podcast_author=None
    )
    
    # Test valid values
    params.episode_rating = "highest"
    assert params.episode_rating == "highest"
    params.episode_rating = "lowest"
    assert params.episode_rating == "lowest"
    params.episode_rating = None
    assert params.episode_rating is None
    
    # Test invalid value
    with pytest.raises(ValueError):
        params.episode_rating = "invalid"


def test_podcast_title_setter():
    params = SortParameters(
        _episode_title=None,
        _episode_duration=None,
        _episode_date=None,
        _episode_rating=None,
        _podcast_title=None,
        _podcast_author=None
    )
    
    # Test valid values
    params.podcast_title = "A-Z"
    assert params.podcast_title == "A-Z"
    params.podcast_title = "Z-A"
    assert params.podcast_title == "Z-A"
    params.podcast_title = None
    assert params.podcast_title is None
    
    # Test invalid value
    with pytest.raises(ValueError):
        params.podcast_title = "invalid"


def test_podcast_author_setter():
    params = SortParameters(
        _episode_title=None,
        _episode_duration=None,
        _episode_date=None,
        _episode_rating=None,
        _podcast_title=None,
        _podcast_author=None
    )
    
    # Test valid values
    params.podcast_author = "A-Z"
    assert params.podcast_author == "A-Z"
    params.podcast_author = "Z-A"
    assert params.podcast_author == "Z-A"
    params.podcast_author = None
    assert params.podcast_author is None
    
    # Test invalid value
    with pytest.raises(ValueError):
        params.podcast_author = "invalid"