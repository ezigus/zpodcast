import re

def is_valid_url(url: str) -> bool:
    """
    Check if a given URL is valid.

    Args:
        url (str): The URL to validate.

    Returns:
        bool: True if the URL is valid, False otherwise.
    """
    # url_regex = re.compile(
    #     r'^(?:http|ftp)s?://'  # http:// or https://
    #     r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    #     r'localhost|'  # localhost...
    #     r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or IP
    #     r'(?::\d+)?'  # optional port
    #     r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    # return bool(re.match(url_regex, url))
