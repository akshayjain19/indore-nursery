"""Fetch Plants / Pots tabs from Google Sheets (service account)."""

from __future__ import annotations

import json
import os

from lib.catalog_sync import SyncError, rows_from_table

DEFAULT_TAB_PLANTS = "Plants"
DEFAULT_TAB_POTS = "Pots"
READ_SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
WRITE_SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def sheets_configured() -> bool:
    return bool(os.environ.get("GOOGLE_SHEETS_SPREADSHEET_ID", "").strip())


def _service_account_info() -> dict:
    raw = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON", "").strip()
    if raw:
        try:
            return json.loads(raw)
        except json.JSONDecodeError as e:
            raise SyncError(f"GOOGLE_SERVICE_ACCOUNT_JSON is not valid JSON: {e}") from e
    path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "").strip()
    if path and os.path.isfile(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    raise SyncError(
        "Google Sheets sync requires GOOGLE_SERVICE_ACCOUNT_JSON or GOOGLE_APPLICATION_CREDENTIALS"
    )


def service_account_email() -> str:
    return str(_service_account_info().get("client_email") or "")


def authorize_client(*, write: bool = False):
    try:
        import gspread
        from google.oauth2.service_account import Credentials
    except ImportError as e:
        raise SyncError(
            "Install Google Sheets dependencies: pip install -r requirements.txt"
        ) from e

    scopes = WRITE_SCOPES if write else READ_SCOPES
    creds = Credentials.from_service_account_info(_service_account_info(), scopes=scopes)
    return gspread.authorize(creds)


def _client():
    return authorize_client(write=False)


def fetch_tab_values(spreadsheet_id: str, tab_name: str) -> list[list]:
    gc = _client()
    try:
        sh = gc.open_by_key(spreadsheet_id)
    except Exception as e:
        raise SyncError(
            f"Cannot open spreadsheet {spreadsheet_id}. "
            "Share the sheet with the service account email (Editor or Viewer). "
            f"Details: {e}"
        ) from e
    try:
        ws = sh.worksheet(tab_name)
    except Exception as e:
        raise SyncError(f"Missing worksheet tab {tab_name!r}: {e}") from e
    return ws.get_all_values()


def load_catalog_rows_from_sheets() -> tuple[list[dict], list[dict], str]:
    spreadsheet_id = os.environ.get("GOOGLE_SHEETS_SPREADSHEET_ID", "").strip()
    if not spreadsheet_id:
        raise SyncError("GOOGLE_SHEETS_SPREADSHEET_ID is not set")
    tab_plants = os.environ.get("GOOGLE_SHEETS_TAB_PLANTS", DEFAULT_TAB_PLANTS).strip() or DEFAULT_TAB_PLANTS
    tab_pots = os.environ.get("GOOGLE_SHEETS_TAB_POTS", DEFAULT_TAB_POTS).strip() or DEFAULT_TAB_POTS
    plant_rows = rows_from_table(fetch_tab_values(spreadsheet_id, tab_plants))
    pot_rows = rows_from_table(fetch_tab_values(spreadsheet_id, tab_pots))
    source = f"google_sheets:{spreadsheet_id}"
    return plant_rows, pot_rows, source
