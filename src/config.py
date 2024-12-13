# src/config.py
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
EMAIL_USERNAME = os.environ.get("EMAIL_USERNAME", "")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD", "")
EMAIL_SERVER = os.environ.get("EMAIL_SERVER", "imap.gmail.com")
EMAIL_FOLDER = os.environ.get("EMAIL_FOLDER", "scholar_alerts")