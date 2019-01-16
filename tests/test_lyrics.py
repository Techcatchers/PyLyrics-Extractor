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

            Songs to try with:
            1. despacito
            2. Mere Rashke Kamar
            3. closer
            4. perfect

            Example for the Output:
            test_song_title = "Mere Rashke Qamar Lyrics - Baadshaho | Rahat Fateh Ali Khan"
            test_Song_lyrics = "Aise lehra ke tu rubaroo aa gayi\n Aise lehra ke tu rubaroo aa gayi\n Dhadkane betahasha tadapane lagin\n Dhadkane betahasha tadapane lagin\n Teer aisa laga dard aisa jagaa\n Teer aisa laga dard aisa jagaa\n Chot dil pe wo khaayi mazaa aa gayaa!\n\nMere rashke qamar…\n Mere rashke qamar tune pehli nazar\n Jab nazar se milaai maza aagaya\n Josh hi josh mein meri aagosh mein\n Aake tu jo samaaai mazaa aa gaya\n\n(Rashk: Jealous/Envy; Qamar: Moon)\n Here “Rashq-e-Qamar” is used for the girl who is so beautiful that even the Moon is jealous of her.\n\n(Mere rashke qamar tune pehli nazar\n Jab nazar se milaai mazaa aagaya\n Jab nazar se milaai mazaa aagaya)\n\nRet hi ret thi mere dil mein bhari\n Ret hi ret thi mere dil mein bhari\n Pyaas hi pyaas thi zindagi ye meri\n Pyaas hi pyaas thi zindagi ye meri\n\nAaj sehraao mein, ishq ke gaaon mein\n Aaj sehraao mein, ishq ke gaaon mein\n Baarishein ghir ke aayin mazaa aa gaya\n\nMere rashke qamar…\n\n(Mere rashke qamar tune pehli nazar\n Jab nazar se milaai maza aa gaya)\n\nRanjha ho gaye, hum Fana ho gaye\n Aise tu muskuraai mazaa aa gaya\n\n(Mere rashke qamar tune pehli nazar\n Jab nazar se milaai maza aa gaya\n Jab nazar se milaai maza aa gaya)\n\nBarq si gir gayi kaam hi kar gayi\n Barq si gir gayi kaam hi kar gayi\n Aag aisi lagaai mazaa aa gaya\n\n"
        """

        # Initilizes the Song_Lyrics class with the required parameters
        extract_lyrics = Song_Lyrics(GCS_API_KEY, GCS_ENGINE_ID)
        try:
            extract_lyrics.get_lyrics("shape of you")
            time.sleep(12)
        except Exception as e:
            print("Error in extracting the song lyrics.\n" + e)

        try:
            extract_lyrics.get_lyrics("tere jaisa yaar kaha")
            time.sleep(15)
        except Exception as e:
            print("Error in autocorrecting the song name.\n" + e)

        # The function checks for title and lyrics when lyrics is found.
        song_title, song_lyrics = extract_lyrics.get_lyrics("asdfghjklzxcvbnm")
        test_song_title = "No lyrics found for asdfghjklzxcvbnm"
        test_Song_lyrics = ''

        self.assertEqual(song_title, test_song_title)
        self.assertEqual(song_lyrics, test_Song_lyrics)


if __name__ == '__main__':
    unittest.main()

# Run this test using: python -m unittest tests.test_lyrics