"""
Helpers Module

This module provides utility functions that are commonly used across the application.

Functions:
    is_valid_url: Validates whether a given string is a properly formatted URL.
"""

import re


def is_valid_url(url: str) -> bool:
    """
    Check if a given URL is valid.

    This function uses a regular expression to validate the format of a URL.

    Args:
        url (str): The URL to validate.

    Returns:
        bool: True if the URL is valid, False otherwise.

    Example:
        >>> is_valid_url("https://example.com")
        True
        >>> is_valid_url("invalid-url")
        False
    """
    url_regex = re.compile(
        r"^(?:http)s?://"  # http:// or https://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
        r"localhost|"  # localhost...
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or IP
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )

    return bool(re.match(url_regex, url))
