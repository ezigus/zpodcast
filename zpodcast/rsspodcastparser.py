import sys
sys.path.append('..')

import feedparser
from zpodcast.opmlparser import parse_opml_file
from zpodcast.podcastepisode import PodcastEpisode



class RSSPodcastParser:
    @staticmethod
    def get_episodes(rss_feed_url: str) -> list[PodcastEpisode]:
        # Parse the RSS feed using feedparser library
        feed = feedparser.parse(rss_feed_url)

        episodes = []
        for entry in feed.entries:
            # Extract relevant information for each episode

            episode = PodcastEpisode(
                title=entry.title,  # Episode title
                description=entry.description,  # Episode description
                pub_date=entry.published,  # Episode published date
                duration=entry.itunes_duration if 'itunes_duration' in entry else None,  # Episode duration
                duration_in_seconds=RSSPodcastParser._convert_duration_to_seconds(
                    entry.itunes_duration) if 'itunes_duration' in entry else None,  # Episode duration in seconds
                audio_url=entry.enclosures[0].href if entry.enclosures else None,  # Episode audio URL
                episode_number=entry.itunes_episode if 'itunes_episode' in entry else None, # Episode number
                guid=entry.guid if 'guid' in entry else None  # Episode GUID
            )
            episodes.append(episode)

        return episodes

    # return the meta data for an RSS feed
    def get_rss_metadata(rss_feed_url: str) -> dict:
        # Parse the RSS feed using feedparser library
        feed_str = feedparser.parse(rss_feed_url)
        podcast_meta = {
            'title': feed_str.feed.title if 'title' in feed_str.feed else None,
            'description': feed_str.feed.description if 'description' in feed_str.feed else None,
            'author': feed_str.feed.author if 'author' in feed_str.feed else None,
            'image': feed_str.feed.image.href if 'image' in feed_str.feed else None
        }
        return podcast_meta
 

    @staticmethod
    def _convert_duration_to_seconds(duration):
        if duration is None:
            return None

        if ':' not in duration:
            return int(duration)

        # Split the duration string into hours, minutes, and seconds
        parts = duration.split(':')
        hours = int(parts[0]) if len(parts) > 0 else 0
        minutes = int(parts[1]) if len(parts) > 1 else 0
        seconds = int(parts[2]) if len(parts) > 2 else 0

        # Calculate the total duration in seconds
        total_seconds = hours * 3600 + minutes * 60 + seconds
        return total_seconds

def main():
    # Specify the path to the OPML file
    opml_file_path = 'test.opml'

    # Retrieve the list of RSS feeds from the OPML file
    rss_feeds = parse_opml_file(opml_file_path)

    # Print all RSS feeds returned
    print("RSS feeds:")
    for rss_feed in rss_feeds:
        print("Title:", rss_feed['title'])
        print("URL:", rss_feed['url'])
        print("Type:", rss_feed['type'])
        print()

    if rss_feeds:
        # Use the first RSS feed from the parsed OPML file
        rss_feed_url = rss_feeds[0]['url']

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


if __name__ == '__main__':
    main()
