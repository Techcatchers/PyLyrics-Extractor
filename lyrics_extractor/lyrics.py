import time
import urllib.parse
import urllib.request
import json
from bs4 import BeautifulSoup


class LyricScraperException(Exception):
    """Handles all lyrics extractor exceptions."""


class _ScraperFactory:
    """All scrapers are defined here."""

    PARAGRAPH_BREAK = '\n\n'
    source_code = None
    title = None

    def __call__(self, source_code, title):
        self.source_code = source_code
        self.title = title

    def _update_title(self, title):
        self.title = title

    def _genius_scraper_method_1(self):
        extract = self.source_code.select(".lyrics")
        if not extract:
            return None

        lyrics = (extract[0].get_text()).replace('<br>', '\n').strip()
        return lyrics

    def _genius_scraper_method_2(self):
        all_extracts = self.source_code.select(
            'div[class*="Lyrics__Container-sc-"]')
        if not all_extracts:
            return None

        lyrics = ''
        for extract in all_extracts:
            for br in extract.find_all("br"):
                br.replace_with("\n")
            lyrics += extract.get_text()

        return lyrics.strip()

    def genius_scraper(self):
        lyrics = self._genius_scraper_method_1() or self._genius_scraper_method_2()
        self._update_title(self.title[:-16])

        return lyrics

    def glamsham_scraper(self):
        extract = self.source_code.find_all('font', class_='general')[5]
        if not extract:
            return None

        for br in extract.find_all("br"):
            br.replace_with("\n")
        lyrics = extract.get_text()
        self._update_title(self.title[:-14].strip())

        return lyrics

    def lyricsbell_scraper(self):
        extract = self.source_code.select(".lyrics-col p")
        if not extract:
            return None

        lyrics = ''
        for i in range(len(extract)):
            lyrics += extract[i].get_text() + self.PARAGRAPH_BREAK

        lyrics = lyrics.replace('<br>', '\n').strip()
        self._update_title(self.title[:-13])
        return lyrics

    def lyricsted_scraper(self):
        extract = self.source_code.select(".lyric-content p")
        if not extract:
            return None

        lyrics = ''
        for i in range(len(extract)):
            lyrics += extract[i].get_text().strip() + self.PARAGRAPH_BREAK

        lyrics = lyrics.replace('<br>', '\n').strip()
        return lyrics

    def lyricsoff_scraper(self):
        extract = self.source_code.select("#main_lyrics p")
        if not extract:
            return None

        lyrics = ''
        for i in range(len(extract)):
            lyrics += extract[i].get_text(separator="\n").strip() + \
                self.PARAGRAPH_BREAK

        return lyrics.strip()

    def lyricsmint_scraper(self):
        extract = self.source_code.find(
            'section', {'id': 'lyrics'}).find_all('p')
        if not extract:
            return None

        lyrics = ''
        for i in range(len(extract)):
            lyrics += extract[i].get_text().strip() + \
                self.PARAGRAPH_BREAK

        return lyrics.strip()

    def kkbox_scraper(self):
        extract = self.source_code.select("div.lyrics > p:nth-of-type(2)")
        if not extract:
            return None
            
        return extract[0].get_text().strip()

    def musixmatch_scraper(self):
        extract = self.source_code.select("div.mxm-lyrics > span")
        if not extract:
            return None

        return extract[0].get_text().strip()


class SongLyrics:
    """
        Takes in Google Custom Search API & Google Engine ID in contructor args.
        Call get_lyrics function with song_name as args to get started.
        Handle raised LyricScraperException by importing it alongside.
    """

    scraper_factory = _ScraperFactory()
    SCRAPERS = {
        "genius": scraper_factory.genius_scraper,
        'glamsham': scraper_factory.glamsham_scraper,
        'lyricsbell': scraper_factory.lyricsbell_scraper,
        'lyricsted': scraper_factory.lyricsted_scraper,
        'lyricsoff': scraper_factory.lyricsoff_scraper,
        'lyricsmint': scraper_factory.lyricsmint_scraper,
        'kkbox': scraper_factory.kkbox_scraper,
        'musixmatch': scraper_factory.musixmatch_scraper,
    }

    def __init__(self, gcs_api_key: str, gcs_engine_id: str):
        if type(gcs_api_key) != str or type(gcs_engine_id) != str:
            raise TypeError("API key and engine ID must be a string.")

        self.GCS_API_KEY = gcs_api_key
        self.GCS_ENGINE_ID = gcs_engine_id

    def __handle_search_request(self, song_name):
        url = "https://www.googleapis.com/customsearch/v1/siterestrict"
        params = {
            'key': self.GCS_API_KEY,
            'cx': self.GCS_ENGINE_ID,
            'q': '{}'.format(song_name),
        }

        response = urllib.request.urlopen(url+'?'+urllib.parse.urlencode(params))
        data = json.loads(response.read().decode())
        return data

    def __extract_lyrics(self, result_url, title):
        # Get the page source code
        req = urllib.request.Request(
            result_url, 
            data=None, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )
        page = urllib.request.urlopen(req)
        source_code = BeautifulSoup(page.read().decode(), 'lxml')

        self.scraper_factory(source_code, title)
        for domain, scraper in self.SCRAPERS.items():
            if domain in result_url:
                lyrics = scraper()

        return lyrics

    def get_lyrics(self, song_name: str) -> dict:
        """
            Fetches and autocorrects (if incorrect) song name.
            Gets URL and title of the top Results.
            Extracts lyrics by using one of the available scrapers.
            Raises LyricScraperException on handling errors.
            Returns dict with title and lyrics.
        """

        data = self.__handle_search_request(song_name)

        spell = data.get('spelling', {}).get('correctedQuery')
        data = (spell and self.__handle_search_request(spell)) or data
        query_results = data.get('items', [])

        # Try scraping lyrics from top results
        for i in range(len(query_results)):
            result_url = query_results[i]["link"]
            title = query_results[i]["title"]
            try:
                lyrics = self.__extract_lyrics(result_url, title)
            except Exception as err:
                raise LyricScraperException(err)

            if lyrics:
                return {
                    "title": self.scraper_factory.title,
                    "lyrics": lyrics
                }

        raise LyricScraperException({"error": "No results found"})
