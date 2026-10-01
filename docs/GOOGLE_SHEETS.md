# Google Sheets catalog (live sync)

Product data (**Plants** and **Pots**) can sync from Google Sheets on every build/deploy. Blog, events copy, and other content still come from JSON/code in the repo.

## 1. Create a Google Cloud service account

1. Open [Google Cloud Console](https://console.cloud.google.com/) → create or select a project.
2. **APIs & Services → Enable APIs** → enable **Google Sheets API**.
3. **APIs & Services → Credentials → Create credentials → Service account**.
4. Create a key: **Keys → Add key → JSON** and download the file.

Keep this JSON secret. Do not commit it to git.

## 2. Create the spreadsheet

**Option A — new empty sheet**

1. Create a blank Google Spreadsheet.
2. Add two tabs named exactly **`Plants`** and **`Pots`** (or set custom names via env vars below).

**Option B — seed from the repo Excel file**

1. Create a blank spreadsheet and copy its **Spreadsheet ID** from the URL.
2. Set env vars (see section 3), then run:

```bash
pip install -r requirements.txt
export GOOGLE_SHEETS_SPREADSHEET_ID="your-spreadsheet-id"
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"
python3 scripts/push_catalog_to_google_sheets.py
```

This uploads `data/excel/indore_nursery_products.xlsx` into the **Plants** and **Pots** tabs.

## 3. Share the sheet with the service account

Open the JSON key and find `"client_email"` (looks like `something@project-id.iam.gserviceaccount.com`).

In Google Sheets: **Share** → add that email as **Editor** (required for push script; **Viewer** is enough for read-only deploy sync).

## 4. Configure environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GOOGLE_SHEETS_SPREADSHEET_ID` | Yes (for Sheets mode) | ID from the spreadsheet URL |
| `GOOGLE_SERVICE_ACCOUNT_JSON` | One of these | Full JSON string (use on Vercel) |
| `GOOGLE_APPLICATION_CREDENTIALS` | One of these | Path to JSON file (local dev) |
| `GOOGLE_SHEETS_TAB_PLANTS` | No | Default `Plants` |
| `GOOGLE_SHEETS_TAB_POTS` | No | Default `Pots` |

Local example:

```bash
cp .env.example .env
# edit .env, then:
set -a && source .env && set +a
python3 scripts/sync_catalog.py
python3 build.py
```

If `GOOGLE_SHEETS_SPREADSHEET_ID` is **not** set, the build uses **`data/excel/indore_nursery_products.xlsx`** as before.

## 5. Live sync on deploy (Vercel)

1. Add the env vars above in **Vercel → Project → Settings → Environment Variables** (paste the whole service account JSON into `GOOGLE_SERVICE_ACCOUNT_JSON`).
2. Deploy from `main` (or your production branch).

`scripts/vercel-build.sh` detects `GOOGLE_SHEETS_SPREADSHEET_ID` and runs a **full** `python3 build.py` (sync → generate → deploy `site/`), even if a prebuilt `site/` exists in git.

Each production deploy pulls the latest sheet data.

## 6. Column layout

Same headers as the Excel workbook (row 1 = headers). See `scripts/migrate_catalog_to_excel.py` (`PLANT_HEADERS`, `POT_HEADERS`) or the existing xlsx file.

## 7. Commands

```bash
python3 scripts/sync_catalog.py          # Sheets if configured, else Excel → data/generated/
python3 scripts/push_catalog_to_google_sheets.py   # Excel → Sheets (one-time / refresh structure)
python3 build.py                         # full site build
```

After sync, check `data/generated/catalog-sync-meta.json` for `source`: `google_sheets:…` or `excel`.

## Troubleshooting

- **Cannot open spreadsheet** — share the sheet with the service account email.
- **Missing worksheet tab** — tab names must match `Plants` / `Pots` (or your env overrides).
- **ERROR: Invalid price** — fix numeric cells in the sheet; prices must be numbers.
- **Deploy still shows old products** — confirm Vercel has env vars on the **Production** environment and redeploy.
