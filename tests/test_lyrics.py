from lyrics_extractor import SongLyrics, LyricScraperException

# NOTE: Env vars will be fetched from lyrics_extractor directory so make sure
# your .env file is inside this directory
from lyrics_extractor.settings import GCS_API_KEY, GCS_ENGINE_ID
import unittest
import time


UNAVAILABLE_SONG_NAME = "sjdfkhs!4353234rjsjkaw@d"
MISSPELLED_SONG_NAME = "sheap of you"
SONG_NAME = "waka waka"


class TestSongLyrics(unittest.TestCase):
    extract_lyrics = None

    def setUp(self):
        self.extract_lyrics = SongLyrics(GCS_API_KEY, GCS_ENGINE_ID)

    def test_unavailable_lyrics(self):
        """
            Random unavailable song name passed.
            Expected custom exception.
        """

        self.assertRaises(
            LyricScraperException,
            self.extract_lyrics.get_lyrics,
            UNAVAILABLE_SONG_NAME
        )

    def test_incorrect_spelled_lyrics(self):
        """
            Misspelled song name passed.
            Expected autocorrection and successful data return.
        """

        data = self.extract_lyrics.get_lyrics(MISSPELLED_SONG_NAME)
        self.assertIn('title', data)
        self.assertIn('lyrics', data)

    def test_lyrics_success(self):
        """
            Correct song name passed.
            Expected successful data return.
        """

        data = self.extract_lyrics.get_lyrics(SONG_NAME)
        self.assertIn('title', data)
        self.assertIn('lyrics', data)


if __name__ == '__main__':
    unittest.main()

# Run this test using: python -m unittest tests.test_lyrics
