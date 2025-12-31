import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', '6d4ffae0888e1d0f492aba5dbc8d6312455dca98b00f34a9cf1b2f9b7dccdc8e')
    GOOGLE_SHEETS_CREDENTIALS_FILE = os.getenv('GOOGLE_SHEETS_CREDENTIALS_FILE', 'credentials.json')
    GOOGLE_SHEETS_CREDENTIALS_JSON = os.getenv('GOOGLE_SHEETS_CREDENTIALS_JSON')
    GOOGLE_SHEET_ID = os.getenv('GOOGLE_SHEET_ID')
