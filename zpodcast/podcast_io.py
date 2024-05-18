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
            

            

        