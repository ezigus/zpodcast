"""
RSS Feed Parser Module

This module provides functionality for retrieving and parsing podcast RSS feeds.
It converts feed entries into structured PodcastEpisode objects and extracts podcast metadata.

Classes:
    RSSPodcastParser: A parser for retrieving and processing podcast data from RSS feeds.

Functions:
    get_episodes: Retrieves and parses episodes from an RSS feed.
    get_rss_metadata: Extracts podcast metadata from an RSS feed.
"""

import feedparser
from zpodcast.parsers.opml import parse_opml_file
from zpodcast.core.episode import PodcastEpisode
from typing import List
import logging


class RSSPodcastParser:
    """
    A parser for retrieving and processing podcast data from RSS feeds.

    This class provides methods to extract episodes and metadata from RSS feeds.
    It handles parsing errors gracefully and logs issues for debugging purposes.

    Methods:
        get_episodes(rss_feed_url: str) -> List[PodcastEpisode]:
            Retrieves and parses episodes from an RSS feed.

        get_rss_metadata(rss_feed_url: str) -> dict:
            Extracts metadata from an RSS feed.

        _convert_duration_to_seconds(duration: str) -> int:
            Converts a duration string into total seconds.
    """

    @staticmethod
    def get_episodes(rss_feed_url: str) -> List[PodcastEpisode]:
        """
        Retrieve and parse episodes from an RSS feed.

        This method uses the feedparser library to parse the RSS feed and extract
        relevant information for each episode, such as title, audio URL, description,
        publication date, duration, episode number, and image URL.

        Args:
            rss_feed_url (str): The URL of the RSS feed.

        Returns:
            List[PodcastEpisode]: A list of parsed podcast episodes.

        Raises:
            ValueError: If the RSS feed URL is invalid or parsing fails.

        Example:
            >>> episodes = RSSPodcastParser.get_episodes("https://example.com/feed.rss")
            >>> for episode in episodes:
            >>>     print(episode.title)
        """
        try:
            # Parse the RSS feed using feedparser library
            feed = feedparser.parse(rss_feed_url)

            if feed.bozo:  # feedparser error
                logging.error(
                    f"Feed parsing error for {rss_feed_url}: {feed.bozo_exception}"
                )
                return []

            episodes = []
            for entry in feed.entries:
                try:
                    # Extract relevant information for each episode
                    episode = PodcastEpisode(
                        title=entry["title"],  # Episode title
                        audio_url=(
                            entry["enclosures"][0]["href"]
                            if entry.get("enclosures")
                            else None
                        ),  # Episode audio URL
                        description=entry["description"],  # Episode description
                        pub_date=entry["published"],  # Episode published date
                        duration=entry.get("itunes_duration"),  # Episode duration
                        episode_number=entry.get("itunes_episode"),  # Episode number
                        image_url=entry.get("image", {}).get(
                            "href"
                        ),  # Episode image URL
                        guid=entry.get("guid"),  # Episode GUID
                    )
                    episodes.append(episode)
                except Exception as e:
                    logging.error(f"Error creating episode from entry: {e}")
                    continue

            return episodes
        except Exception as e:
            logging.error(f"Error parsing RSS feed {rss_feed_url}: {e}")
            return []

    # return the meta data for an RSS feed
    @staticmethod
    def get_rss_metadata(rss_feed_url: str) -> dict:
        """
        Extract metadata from an RSS feed.

        This method retrieves metadata such as the podcast title, description,
        author, and image URL from the RSS feed.

        Args:
            rss_feed_url (str): The URL of the RSS feed.

        Returns:
            dict: A dictionary containing metadata such as title, description, author, and image URL.

        Raises:
            ValueError: If the RSS feed URL is invalid or parsing fails.

        Example:
            >>> metadata = RSSPodcastParser.get_rss_metadata("https://example.com/feed.rss")
            >>> print(metadata["title"])
        """
        try:
            # Parse the RSS feed using feedparser library
            feed = feedparser.parse(rss_feed_url)

            if feed.bozo:  # feedparser error
                logging.error(
                    f"Feed parsing error for {rss_feed_url}: {feed.bozo_exception}"
                )
                return {}

            # Get feed metadata
            feed_data = feed.feed
            podcast_meta = {
                "title": feed_data.get("title"),
                "description": feed_data.get("description"),
                "author": feed_data.get("author"),
                "image": feed_data.get("image", {}).get("href"),
            }
            return podcast_meta
        except Exception as e:
            logging.error(f"Error getting RSS metadata for {rss_feed_url}: {e}")
            return {}

    @staticmethod
    def _convert_duration_to_seconds(duration: str) -> int:
        """
        Convert a duration string into total seconds.

        This method supports various duration formats, including plain seconds,
        MM:SS, and HH:MM:SS.

        Args:
            duration (str): The duration string to convert.

        Returns:
            int: The total duration in seconds.

        Example:
            >>> RSSPodcastParser._convert_duration_to_seconds("01:30:00")
            5400
        """
        if duration is None:
            return None

        if ":" not in duration:
            return int(duration)

        # Split the duration string into hours, minutes, and seconds
        parts = duration.split(":")
        hours = int(parts[0]) if len(parts) > 0 else 0
        minutes = int(parts[1]) if len(parts) > 1 else 0
        seconds = int(parts[2]) if len(parts) > 2 else 0

        # Calculate the total duration in seconds
        total_seconds = hours * 3600 + minutes * 60 + seconds
        return total_seconds


def main():
    """
    Demonstrate the usage of the RSSPodcastParser class.

    This function parses an OPML file to retrieve a list of RSS feeds, extracts
    episodes from the first feed, and prints the details of each episode.

    Example:
        >>> main()
    """
    # Specify the path to the OPML file
    opml_file_path = "test.opml"

    # Retrieve the list of RSS feeds from the OPML file
    rss_feeds = parse_opml_file(opml_file_path)

    # Print all RSS feeds returned
    print("RSS feeds:")
    for rss_feed in rss_feeds:
        print("Title:", rss_feed["title"])
        print("URL:", rss_feed["url"])
        print("Type:", rss_feed["type"])
        print()

    if rss_feeds:
        # Use the first RSS feed from the parsed OPML file
        rss_feed_url = rss_feeds[0]["url"]

        # Retrieve the list of episodes from the RSS feed
        episodes = RSSPodcastParser.get_episodes(rss_feed_url)

        # Print each episode
        for episode in episodes:
            print("Title:", episode.title)
            print("Description:", episode.description)
            print("Published Date:", episode.pub_date)
            print("Audio URL:", episode.audio_url)
            print("Episode Number:", episode.episode_number)
            print("Duration:", episode.duration)
            print("Duration in Seconds:", episode.duration_in_seconds)
            print()
    else:
        print("No RSS feeds found in the OPML file.")


if __name__ == "__main__":
    main()
