import unittest
from typing import Optional

from zpodcast.sortparameters import SortParameters

class TestSortParameters(unittest.TestCase):
    def test_episode_title(self):
        sort_params = SortParameters()
        sort_params.episode_title = "A-Z"
        self.assertEqual(sort_params.episode_title, "A-Z")

    def test_episode_duration(self):
        sort_params = SortParameters()
        sort_params.episode_duration = "ShortToLong"
        self.assertEqual(sort_params.episode_duration, "ShortToLong")

    def test_episode_date(self):
        sort_params = SortParameters()
        sort_params.episode_date = "Earliest"
        self.assertEqual(sort_params.episode_date, "Earliest")

    def test_episode_rating(self):
        sort_params = SortParameters()
        sort_params.episode_rating = "highest"
        self.assertEqual(sort_params.episode_rating, "highest")

    def test_episode_tags(self):
        sort_params = SortParameters()
        sort_params.episode_tags = ["tag1", "tag2"]
        self.assertEqual(sort_params.episode_tags, ["tag1", "tag2"])

    def test_podcast_title(self):
        sort_params = SortParameters()
        sort_params.podcast_title = "A-Z"
        self.assertEqual(sort_params.podcast_title, "A-Z")

    def test_podcast_author(self):
        sort_params = SortParameters()
        sort_params.podcast_author = "A-Z"
        self.assertEqual(sort_params.podcast_author, "A-Z")

    def test_podcast_category(self):
        sort_params = SortParameters()
        sort_params.podcast_category = "Technology"
        self.assertEqual(sort_params.podcast_category, "Technology")

if __name__ == '__main__':
    unittest.main()
