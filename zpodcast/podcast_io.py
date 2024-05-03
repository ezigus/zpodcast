from podcastdata import PodcastData
import json

class Podcast_IO:
    """
    Initializes a new instance of the SavePodcast class.

    Args:
        podcast_data (PodcastData): The podcast data to save.
    """
    def __init__(self, filename:str):
        self.filename = filename

    def save(self, podcasts: [PodcastData]) --> bool:
        """
        Saves all podcast data using a serialization in json format to a local file - this method overwrites the file each time it is called 
        it should also store all of the podcast episodes data it knows about from the podcast data object
        """

        # serialize the podcastdata object
        json_podcast = json.dumps(podcasts, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        print (json_podcast)

        # write the dictionary to a file
        with open(self.filename, 'w') as f:
            f.write(json_podcast

    def load(self) -> [PodcastData]:
        
        

        