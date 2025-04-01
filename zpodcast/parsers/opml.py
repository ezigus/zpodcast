import os
from typing import List, Dict
import xml.etree.ElementTree as ET


"""
Parse an OPML file

Returns:
    returns a parsed OPML file with 3 variables - title, rss_url and type
"""


def parse_opml_file(file_path: str) -> List[Dict[str, str]]:
    """
    Parse an OPML file to extract podcast RSS feeds.

    Args:
        file_path (str): Path to the OPML file

    Returns:
        List[Dict[str, str]]: List of dictionaries containing podcast feed information
    """
    variables = []  # List to store the parsed variables

    if not os.path.isfile(file_path):
        # print(f"File not found: {file_path}")
        return variables

    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Parse the OPML file and store the data in variables
        for outline in root.iter("outline"):
            # if outline.attrib.get("type") != "rss":
            RSSTitle = outline.attrib.get("title")
            RSSUrl = outline.attrib.get("xmlUrl")
            feed_type = outline.attrib.get("type")
            if RSSTitle and RSSUrl and feed_type:
                variables.append(
                    {"title": RSSTitle, "rss_url": RSSUrl, "type": feed_type}
                )
            # else:
            #     print("type=",outline.attrib.get("type"))

    except ET.ParseError as e:
        print(f"Error parsing OPML file: {e}")

    return variables
