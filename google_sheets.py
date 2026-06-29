import gspread
from google.oauth2.service_account import Credentials
from config import GOOGLE_CREDENTIALS_FILE, GOOGLE_SHEET_NAME

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

_client = None
_sheet = None


def _connect():
    global _client, _sheet

    if _client and _sheet:
        return

    creds = Credentials.from_service_account_file(
        GOOGLE_CREDENTIALS_FILE,
        scopes=SCOPES
    )

    _client = gspread.authorize(creds)
    _sheet = _client.open(GOOGLE_SHEET_NAME).sheet1

    # Add header if empty
    if not _sheet.get_all_values():
        _sheet.append_row([
            "Search",
            "Title",
            "Price",
            "URL",
            "Seller",
            "Item ID",
            "Timestamp"
        ])


def append_row(row):
    _connect()
    _sheet.append_row(row)
