import os

from dotenv import load_dotenv

load_dotenv()

APP_ENV = os.getenv("APP_ENV", "development")
BASE_URL = os.environ["BASE_URL"].rstrip("/")
API_KEY = os.environ["API_KEY"]
