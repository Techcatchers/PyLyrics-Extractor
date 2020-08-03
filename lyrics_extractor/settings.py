from os.path import join, dirname
from dotenv import load_dotenv
import os

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Gets env vars (.env file) from lyrics_extractor directory
GCS_API_KEY = os.getenv("GCS_API_KEY")
GCS_ENGINE_ID = os.getenv("GCS_ENGINE_ID")
