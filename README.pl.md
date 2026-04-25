# Car Expense Tracker Bot

> 🇬🇧 [English](README.md) · 🇺🇦 [Українська](README.uk.md)

Bot Telegram do śledzenia wydatków na samochód. Zapisuje wszystko w Google Sheets i wylicza koszt kilometra, żebyś wiedział pełny obraz przy sprzedaży.

## Co śledzi

- **Paliwo** — przebieg, litry, pełny/częściowy bak, cena
- **Serwis / naprawa** — opis i koszt
- **Ubezpieczenie** — rodzaj i kwota
- **Podatki / opłaty** — rodzaj i kwota
- **Parking** — miejsce i koszt
- **Inne** — dowolny wydatek

Kwotę można podać w dowolnej walucie (`250`, `10 EUR`, `500 CZK`, `8.50 GBP` …) — automatycznie przeliczana na walutę bazową według kursów ECB.

`/stats` pokazuje koszt kilometra uwzględniając wszystkie wydatki łącznie z ceną zakupu.

---

## Konfiguracja (jednorazowo)

### 1. Bot Telegram

1. Otwórz [@BotFather](https://t.me/BotFather) w Telegramie
2. Wyślij `/newbot`, podaj nazwę i username
3. Zapisz token — wygląda jak `123456789:AAFxxxxxxxxxxxxxxxx`

### 2. Projekt Google Cloud

1. Przejdź do [console.cloud.google.com](https://console.cloud.google.com)
2. Utwórz nowy projekt (lub użyj istniejącego)
3. **APIs & Services → Library** — włącz:
   - **Google Sheets API**
   - **Google Drive API**

### 3. Service Account

1. **APIs & Services → Credentials → Create Credentials → Service Account**
2. Podaj nazwę, kliknij **Done**
3. Kliknij konto → zakładka **Keys** → **Add Key → Create new key → JSON**
4. Zmień nazwę pobranego pliku na `credentials.json` i umieść go obok `bot.py`
5. Skopiuj email konta serwisowego (wygląda jak `name@project.iam.gserviceaccount.com`)

### 4. Google Spreadsheet

1. Przejdź do [sheets.google.com](https://sheets.google.com) → utwórz nowy arkusz
2. Kliknij **Share** → wklej email konta serwisowego → rola **Editor** → **Share**
3. Skopiuj ID arkusza z URL: `https://docs.google.com/spreadsheets/d/**ID_TUTAJ**/edit`

### 5. Konfiguracja

```bash
cp .env.example .env
```

Edytuj `.env`:

```env
TELEGRAM_TOKEN=token_od_BotFather
SPREADSHEET_ID=id_arkusza_z_url
GOOGLE_CREDENTIALS_FILE=credentials.json
ALLOWED_USER_IDS=123456789,987654321
BASE_CURRENCY=PLN
LANGUAGE=pl
```

Swoje ID Telegrama znajdziesz przez [@userinfobot](https://t.me/userinfobot).

### 6. Uruchomienie

```bash
# Zbuduj obraz
docker compose build

# Uruchom (w tle, automatycznie restartuje)
docker compose up -d
```

Przydatne komendy:

```bash
docker compose logs -f      # live logi
docker compose restart      # restart
docker compose down         # zatrzymaj i usuń kontener
```

---

## Komendy

| Komenda | Opis |
|---------|------|
| `/start` | Powitanie + konfiguracja auta (pierwsze uruchomienie) |
| `/setup` | Zmień dane auta |
| `/fuel` | Zapisz tankowanie |
| `/service` | Serwis lub naprawa |
| `/insurance` | Ubezpieczenie |
| `/tax` | Podatki / opłaty |
| `/parking` | Parking |
| `/other` | Inne wydatki |
| `/stats` | Statystyki: wydatki, km/l, koszt kilometra |
| `/cancel` | Anuluj bieżącą akcję |

---

## Struktura Google Sheets

Bot tworzy dwa arkusze automatycznie:

- **Car** — marka, model, rok, data zakupu, początkowy przebieg, cena zakupu, pojemność baku
- **Expenses** — wszystkie wydatki z datą, kategorią, przebiegiem, kwotą oryginalną, przeliczoną i osobą, która wprowadziła

---

## Obliczanie zużycia paliwa

Spalanie (km/l) jest obliczane tylko między dwoma **pełnymi** tankowaniami.
Częściowe tankowania są wliczane do łącznej liczby litrów, ale nie przerywają segmentu obliczeń.
