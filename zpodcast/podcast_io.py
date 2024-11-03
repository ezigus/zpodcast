from podcastdata import PodcastData
import json
import xml.etree.ElementTree as ET

class Podcast_IO:
    """
    Initializes a new instance of the SavePodcast class.

    Args:
        podcast_data (PodcastData): The podcast data to save.
    """
    def __init__(self, filename:str):
        self.filename = filename

    def save(self, podcasts: [PodcastData]) -> bool:
        """
        Saves all podcast data using a serialization in json format to a local file - this method overwrites the file each time it is called 
        it should also store all of the podcast episodes data it knows about from the podcast data object
        """

        # serialize the podcastdata object
        json_podcast = json.dumps(podcasts, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        print (json_podcast)

        # write the dictionary to a file
        with open(self.filename, 'w') as f:
            f.write(json_podcast)
                    
        return True

    def load(self,) -> [PodcastData]:
        """ 
        read from the file and populate podcast data objects with the data found in the json file
        """
        
        #read the json file
        with open(self.filename, 'r') as f:
            data = json.load(f)
            
        # create a list of podcast data objects with the data loaded from the json file, converting the json into podcast data objects
        podcast_data = []
        for podcast in data:
            podcast_data.append(PodcastData(**podcast))
            
        return podcast_data

    def save_as_opml(self, podcasts: [PodcastData]) -> bool:
        """
        Saves the full list of podcasts as OPML.
        """
        root = ET.Element("opml", version="2.0")
        head = ET.SubElement(root, "head")
        title = ET.SubElement(head, "title")
        title.text = "Podcast Subscriptions"
        body = ET.SubElement(root, "body")

        for podcast in podcasts:
            outline = ET.SubElement(body, "outline", type="rss", text=podcast.title, title=podcast.title, xmlUrl=podcast.podcast_url, htmlUrl=podcast.podcast_url)

        tree = ET.ElementTree(root)
        tree.write(self.filename, encoding="utf-8", xml_declaration=True)

        return True
