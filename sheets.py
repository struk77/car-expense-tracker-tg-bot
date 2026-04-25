from __future__ import annotations

import gspread
from google.oauth2.service_account import Credentials
from config import GOOGLE_CREDENTIALS_FILE, SPREADSHEET_ID

_SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

_client: gspread.Client | None = None
_spreadsheet: gspread.Spreadsheet | None = None


def _get_spreadsheet() -> gspread.Spreadsheet:
    global _client, _spreadsheet
    if _spreadsheet is None:
        creds = Credentials.from_service_account_file(GOOGLE_CREDENTIALS_FILE, scopes=_SCOPES)
        _client = gspread.authorize(creds)
        _spreadsheet = _client.open_by_key(SPREADSHEET_ID)
    return _spreadsheet


def _get_or_create_sheet(name: str, headers: list[str]) -> gspread.Worksheet:
    ss = _get_spreadsheet()
    try:
        ws = ss.worksheet(name)
    except gspread.WorksheetNotFound:
        ws = ss.add_worksheet(title=name, rows=1000, cols=len(headers))
        ws.append_row(headers)
    return ws


# ── Car info ──────────────────────────────────────────────────────────────────

CAR_HEADERS = ["field", "value"]
EXPENSE_HEADERS = [
    "date", "category", "odometer_km", "liters", "full_tank",
    "currency", "original_amount", "pln_amount", "price_per_liter_pln", "notes", "entered_by",
]


def get_car_info() -> dict | None:
    ws = _get_or_create_sheet("Car", CAR_HEADERS)
    rows = ws.get_all_values()
    if len(rows) <= 1:
        return None
    return {row[0]: row[1] for row in rows[1:] if len(row) >= 2}


def save_car_info(info: dict) -> None:
    ws = _get_or_create_sheet("Car", CAR_HEADERS)
    ws.clear()
    ws.append_row(CAR_HEADERS)
    for field, value in info.items():
        ws.append_row([field, str(value)])


# ── Expenses ──────────────────────────────────────────────────────────────────

def add_expense(row: dict) -> None:
    ws = _get_or_create_sheet("Expenses", EXPENSE_HEADERS)
    ws.append_row([str(row.get(h, "")) for h in EXPENSE_HEADERS])


def get_all_expenses() -> list[dict]:
    ws = _get_or_create_sheet("Expenses", EXPENSE_HEADERS)
    rows = ws.get_all_records()
    return rows


def get_fuel_rows() -> list[dict]:
    return [r for r in get_all_expenses() if r.get("category") == "fuel"]
