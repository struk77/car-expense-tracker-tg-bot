# Car Expense Tracker Bot

> 🇬🇧 [English](README.md) · 🇵🇱 [Polski](README.pl.md)

Telegram бот для відстеження витрат на автомобіль. Зберігає все в Google Sheets і рахує вартість кілометра, щоб знати повну картину при продажу.

## Що відстежує

- **Пальне** — пробіг, літри, повний/частковий бак, ціна
- **Сервіс / ремонт** — опис і вартість
- **Страховка** — тип і сума
- **Податки / збори** — вид і сума
- **Паркінг** — місце і вартість
- **Інше** — будь-яка витрата

Суму можна вводити в будь-якій валюті (`250`, `10 EUR`, `500 CZK`, `8.50 GBP` …) — автоматично конвертується в базову валюту через курси ECB.

`/stats` показує вартість кілометра з урахуванням всіх витрат, включно з ціною покупки.

---

## Налаштування (один раз)

### 1. Telegram Bot

1. Відкрийте [@BotFather](https://t.me/BotFather) у Telegram
2. Надішліть `/newbot`, задайте ім'я та username
3. Збережіть токен — він виглядає як `123456789:AAFxxxxxxxxxxxxxxxx`

### 2. Google Cloud проект

1. Відкрийте [console.cloud.google.com](https://console.cloud.google.com)
2. Створіть новий проект (або використайте існуючий)
3. **APIs & Services → Library** — увімкніть:
   - **Google Sheets API**
   - **Google Drive API**

### 3. Service Account

1. **APIs & Services → Credentials → Create Credentials → Service Account**
2. Задайте назву, натисніть **Done**
3. Клікніть на акаунт → вкладка **Keys** → **Add Key → Create new key → JSON**
4. Перейменуйте завантажений файл на `credentials.json` і покладіть поруч з `bot.py`
5. Скопіюйте email сервіс-акаунту (виглядає як `name@project.iam.gserviceaccount.com`)

### 4. Google Spreadsheet

1. Відкрийте [sheets.google.com](https://sheets.google.com) → створіть нову таблицю
2. Натисніть **Share** → вставте email сервіс-акаунту → роль **Editor** → **Share**
3. Скопіюйте ID таблиці з URL: `https://docs.google.com/spreadsheets/d/**ID_ТУТ**/edit`

### 5. Конфігурація

```bash
cp .env.example .env
```

Відредагуйте `.env`:

```env
TELEGRAM_TOKEN=ваш_токен_від_BotFather
SPREADSHEET_ID=id_таблиці_з_URL
GOOGLE_CREDENTIALS_FILE=credentials.json
ALLOWED_USER_IDS=123456789,987654321
BASE_CURRENCY=PLN
LANGUAGE=uk
```

Свій Telegram ID дізнайтесь через [@userinfobot](https://t.me/userinfobot).

### 6. Запуск

```bash
# Зібрати образ
docker compose build

# Запустити (у фоні, перезапускається автоматично)
docker compose up -d
```

Корисні команди:

```bash
docker compose logs -f      # live логи
docker compose restart      # перезапуск
docker compose down         # зупинити і видалити контейнер
```

---

## Команди

| Команда | Опис |
|---------|------|
| `/start` | Початок + налаштування авто (перший запуск) |
| `/setup` | Змінити дані авто |
| `/fuel` | Записати заправку |
| `/service` | Сервіс або ремонт |
| `/insurance` | Страховка |
| `/tax` | Податки / збори |
| `/parking` | Паркінг |
| `/other` | Інші витрати |
| `/stats` | Статистика: витрати, км/л, вартість кілометра |
| `/cancel` | Скасувати поточну дію |

---

## Структура Google Sheets

Бот створює два аркуші автоматично:

- **Car** — марка, модель, рік, дата покупки, початковий пробіг, ціна покупки, об'єм бака
- **Expenses** — всі витрати з датою, категорією, пробігом, оригінальною сумою, конвертованою сумою та ім'ям того, хто вніс

---

## Розрахунок ефективності

Витрата пального (км/л) рахується тільки між двома **повними** баками.
Часткові заправки враховуються в літражі, але не розривають сегмент розрахунку.
