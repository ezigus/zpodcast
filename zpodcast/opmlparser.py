
import os
from typing import List, Dict

class OPMLParser:
    @staticmethod
    def parse_opml_file(file_path: str) -> List[Dict[str, str]]:
        import xml.etree.ElementTree as ET
        variables = []  # List to store the parsed variables

        if not os.path.isfile(file_path):
            print(f"File not found: {file_path}")
            return variables

        try:
            tree = ET.parse(file_path)
            root = tree.getroot()

            # Parse the OPML file and store the data in variables
            for outline in root.iter("outline"):
                if outline.attrib.get("type") != "rss":
                    RSSTitle = outline.attrib.get("title")
                    RSSUrl = outline.attrib.get("xmlUrl")
                    feed_type = outline.attrib.get("type")
                    if RSSTitle and RSSUrl and feed_type:
                        variables.append({"title": RSSTitle, "url": RSSUrl, "type": feed_type})

        except ET.ParseError as e:
            print(f"Error parsing OPML file: {e}")

        return variables


def main() -> None:
    file_path = "data/test.opml"
    rss_urls = OPMLParser.parse_opml_file(file_path)
    
    for feed in rss_urls:
        title = feed["title"]
        url = feed["url"]
        feed_type = feed["XXtypeXX"]
        print(f"Title: {title}, RSS URL: {url}, Feed Type: {feed_type}")


if __name__ == "__main__":
    main()
