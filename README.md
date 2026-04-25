# Car Expense Tracker Bot

> 🇺🇦 [Українська](README.uk.md) · 🇵🇱 [Polski](README.pl.md)

A Telegram bot for tracking car expenses. Stores everything in Google Sheets and calculates cost per kilometre so you know the full picture when you sell.

## What it tracks

- **Fuel** — odometer, litres, full/partial tank, price
- **Service / repair** — description and cost
- **Insurance** — type and amount
- **Taxes / fees** — type and amount
- **Parking** — location and cost
- **Other** — any expense

Amounts can be entered in any currency (`250`, `10 EUR`, `500 CZK`, `8.50 GBP` …) — automatically converted to the base currency via ECB rates.

`/stats` shows cost per km factoring in all expenses including the purchase price.

---

## Setup (one time)

### 1. Telegram Bot

1. Open [@BotFather](https://t.me/BotFather) in Telegram
2. Send `/newbot`, choose a name and username
3. Save the token — it looks like `123456789:AAFxxxxxxxxxxxxxxxx`

### 2. Google Cloud project

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create a new project (or use an existing one)
3. **APIs & Services → Library** — enable:
   - **Google Sheets API**
   - **Google Drive API**

### 3. Service Account

1. **APIs & Services → Credentials → Create Credentials → Service Account**
2. Give it a name, click **Done**
3. Click the account → **Keys** tab → **Add Key → Create new key → JSON**
4. Rename the downloaded file to `credentials.json` and place it next to `bot.py`
5. Copy the service account email (looks like `name@project.iam.gserviceaccount.com`)

### 4. Google Spreadsheet

1. Go to [sheets.google.com](https://sheets.google.com) → create a new spreadsheet
2. Click **Share** → paste the service account email → role **Editor** → **Share**
3. Copy the spreadsheet ID from the URL: `https://docs.google.com/spreadsheets/d/**ID_HERE**/edit`

### 5. Configuration

```bash
cp .env.example .env
```

Edit `.env`:

```env
TELEGRAM_TOKEN=your_token_from_BotFather
SPREADSHEET_ID=spreadsheet_id_from_url
GOOGLE_CREDENTIALS_FILE=credentials.json
ALLOWED_USER_IDS=123456789,987654321
BASE_CURRENCY=PLN
LANGUAGE=en
```

Get your Telegram user ID from [@userinfobot](https://t.me/userinfobot).

### 6. Run

```bash
# Build the image
docker compose build

# Start (runs in background, restarts automatically)
docker compose up -d
```

Useful commands:

```bash
docker compose logs -f      # live logs
docker compose restart      # restart
docker compose down         # stop and remove container
```

---

## Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome + first-time car setup |
| `/setup` | Update car info |
| `/fuel` | Log a fuel stop |
| `/service` | Log service or repair |
| `/insurance` | Log insurance payment |
| `/tax` | Log taxes or fees |
| `/parking` | Log parking |
| `/other` | Log any other expense |
| `/stats` | Statistics: total spend, km/L, cost per km |
| `/cancel` | Cancel current action |

---

## Google Sheets structure

The bot creates two sheets automatically:

- **Car** — make, model, year, purchase date, starting odometer, purchase price, tank size
- **Expenses** — every expense with date, category, odometer, original amount, converted amount, and who entered it

---

## Fuel efficiency calculation

Consumption (km/L) is calculated only between two **full** tank fill-ups.
Partial fills count toward the litre total but don't break the segment.
