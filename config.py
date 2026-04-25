import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
SPREADSHEET_ID = os.environ["SPREADSHEET_ID"]
GOOGLE_CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")
ALLOWED_USER_IDS = {
    int(uid.strip())
    for uid in os.environ["ALLOWED_USER_IDS"].split(",")
    if uid.strip()
}

BASE_CURRENCY = os.getenv("BASE_CURRENCY", "PLN")
LANGUAGE = os.getenv("LANGUAGE", "uk")

CATEGORIES = {
    "service": "Сервіс/Ремонт",
    "insurance": "Страховка",
    "tax": "Податки/Збори",
    "parking": "Паркінг",
    "other": "Інше",
}
