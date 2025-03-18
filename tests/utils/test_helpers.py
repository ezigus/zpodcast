import pytest
from zpodcast.utils.helpers import is_valid_url

def test_is_valid_url():
    # Test valid URLs
    assert is_valid_url("https://example.com")
    assert is_valid_url("http://example.com")
    assert is_valid_url("https://example.com/path")
    assert is_valid_url("https://example.com/path?param=value")
    assert is_valid_url("https://sub.example.com")
    
    # Test invalid URLs
    assert not is_valid_url("not a url")
    assert not is_valid_url("ftp://example.com")  # Only http/https allowed
    assert not is_valid_url("")
    assert not is_valid_url("http://")  # Missing domain
    assert not is_valid_url("https://")  # Missing domain 