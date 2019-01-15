from src.lyrics_extractor import Song_Lyrics
from src.settings import GCS_API_KEY, GCS_ENGINE_ID
import unittest
import time


class TestSongLyrics(unittest.TestCase):
    def test_Song_Lyrics(self):
        """
            Calculates for time taken for fetching song lyrics.
            In my testing for fetching 6 song lyrics, it took on an average of 3 secs.
            Some song spellings here were intentionally made wrong just to test the autocorrection feature.
        """

        # Initilizes the Song_Lyrics class with the required parameters
        extract_lyrics = Song_Lyrics(GCS_API_KEY, GCS_ENGINE_ID)
        extract_lyrics.get_lyrics("shape of you")
        time.sleep(60)
        extract_lyrics.get_lyrics("tere jaisa yaar kaha")
        # time.sleep(60)
        # extract_lyrics.get_lyrics("despacito")
        # time.sleep(60)
        # extract_lyrics.get_lyrics("Perfect")
        # time.sleep(60)
        # extract_lyrics.get_lyrics("Closer")
        # time.sleep(60)
        # extract_lyrics.get_lyrics("Mere Rashke Kamar")

        # The function returns title and lyrics
        song_title, song_lyrics = extract_lyrics.get_lyrics("Mere Rashke Kamar")
        print(song_title, song_lyrics)


if __name__ == '__main__':
    unittest.main()

# Run this test using: python -m unittest tests.test_lyrics