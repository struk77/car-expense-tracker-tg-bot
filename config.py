import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
SPREADSHEET_ID = os.environ["SPREADSHEET_ID"]
GOOGLE_CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")
# TODO: missing ALLOWED_USER_IDS crashes with KeyError; add a friendlier startup error
ALLOWED_USER_IDS = {
    int(uid.strip())
    for uid in os.environ["ALLOWED_USER_IDS"].split(",")
    if uid.strip()
}

BASE_CURRENCY = os.getenv("BASE_CURRENCY", "PLN")
LANGUAGE = os.getenv("LANGUAGE", "uk")

EXPENSE_CATEGORIES = ["service", "insurance", "tax", "parking", "other"]
