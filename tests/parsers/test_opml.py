from zpodcast.parsers.opml import parse_opml_file


def test_parse_opml_file():
    file_path = "tests/data/unit.opml"
    
    rss = parse_opml_file(file_path)
    
    assert rss == [
        {
            "title": "Stuff You Should Know",
            "rss_url": "https://feeds.megaphone.fm/stuffyoushouldknow",
            "type": "rss"
        },
        {
            "title": "Richard Herring's Leicester Square Theatre Podcast",
            "rss_url": "http://feeds.feedburner.com/RichardHerringLSTPodcast",
            "type": "rss"
        },
        {
            "title": "TV Talk Machine",
            "rss_url": "http://feeds.theincomparable.com/tvtm",
            "type": "rss"
        },
        {
            "title": "TV Talk Machine2",
            "rss_url": "http://feeds.theincomparable.com/tvtm",
            "type": "rss"
        },        
        {
            "title": "TV Talk Machine5",
            "rss_url": "http://feeds.theincomparable.com/tvtm",
            "type": "rss"
        },
    ]
