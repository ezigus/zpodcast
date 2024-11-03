import pytest
import xml.etree.ElementTree as ET
from zpodcast.podcast_io import Podcast_IO
from zpodcast.podcastdata import PodcastData
from zpodcast.podcastlist import PodcastList

def test_save_as_opml():
    podcast1 = PodcastData(
        title="Podcast 1",
        podcast_url="http://example.com/podcast1.rss",
        host="Host 1",
        description="Description 1",
        episodes=PodcastList(),
        podcast_priority=5,
        image_url="http://example.com/image1.jpg"
    )
    podcast2 = PodcastData(
        title="Podcast 2",
        podcast_url="http://example.com/podcast2.rss",
        host="Host 2",
        description="Description 2",
        episodes=PodcastList(),
        podcast_priority=5,
        image_url="http://example.com/image2.jpg"
    )
    podcasts = [podcast1, podcast2]
    podcast_io = Podcast_IO("test.opml")
    podcast_io.save_as_opml(podcasts)

    tree = ET.parse("test.opml")
    root = tree.getroot()

    assert root.tag == "opml"
    assert root.attrib["version"] == "2.0"

    head = root.find("head")
    assert head is not None
    assert head.find("title").text == "Podcast Subscriptions"

    body = root.find("body")
    assert body is not None
    outlines = body.findall("outline")
    assert len(outlines) == 2

    assert outlines[0].attrib["title"] == "Podcast 1"
    assert outlines[0].attrib["xmlUrl"] == "http://example.com/podcast1.rss"
    assert outlines[1].attrib["title"] == "Podcast 2"
    assert outlines[1].attrib["xmlUrl"] == "http://example.com/podcast2.rss"
