from config import LANGUAGE

_STRINGS: dict[str, dict[str, str]] = {
    "uk": {
        # auth
        "no_access": "⛔ Немає доступу.",
        # setup
        "start_welcome": "Привіт! Відстежую витрати для {make} {model}.",
        "start_first_time": "Привіт! Давайте налаштуємо трекер.\n\nМарка автомобіля?",
        "setup_update": "Оновлення даних авто.\n\nМарка?",
        "commands_menu": (
            "/fuel — заправка\n"
            "/service — сервіс/ремонт\n"
            "/insurance — страховка\n"
            "/tax — податки/збори\n"
            "/parking — паркінг\n"
            "/other — інше\n"
            "/stats — статистика\n"
            "/setup — змінити дані авто"
        ),
        "ask_make": "Марка автомобіля?",
        "ask_model": "Модель?",
        "ask_year": "Рік випуску?",
        "err_year": "Введіть коректний рік (наприклад 2023).",
        "ask_odo_start": "Поточний пробіг при покупці (км)?",
        "err_odo": "Введіть число км, наприклад: 15000",
        "ask_purchase_price": "Ціна покупки ({currency})?",
        "err_price": "Введіть суму, наприклад: 85000",
        "ask_tank_size": "Об'єм бака (літри)?",
        "err_tank_size": "Введіть коректний об'єм, наприклад: 55",
        "setup_done": "Збережено! {make} {model}, бак {tank}л.\n\nТепер можна вносити витрати:",
        "cancelled": "Скасовано.",
        # fuel
        "ask_odo": "Поточний пробіг (км)?",
        "err_odo_number": "Введіть число, наприклад: 15320",
        "ask_liters": "Скільки літрів залили?",
        "err_liters": "Введіть кількість літрів, наприклад: 42.5",
        "err_tank_overflow": "Увага: {liters}л більше ніж об'єм бака ({tank}л). Перевірте і введіть знову.",
        "ask_full_tank": "Бак залитий вщерть?",
        "btn_full_yes": "Так — повний",
        "btn_full_no": "Ні — частковий",
        "label_full": "повний бак",
        "label_partial": "частковий",
        "cat_fuel": "Пальне",
        "fuel_saved": (
            "Збережено!\n"
            "Пробіг: {odo} км\n"
            "Залито: {liters} л ({full_label})\n"
            "Сплачено: {amount} {currency}{conv_note}\n"
            "Ціна за літр: {price} {base_currency}/л"
        ),
        # amount input
        "amount_hint": "Сума в {base_currency}, або з кодом валюти: «10 EUR», «500 CZK», «8.50 GBP»",
        "err_amount": "Не розумію. {hint}",
        "err_unknown_currency": "Невідома валюта «{code}». {hint}",
        # expense
        "ask_desc": "{label} — короткий опис витрати?",
        "ask_odo_optional": "Пробіг зараз (км)? Або /skip щоб пропустити.",
        "err_odo_or_skip": "Введіть число км або /skip.",
        "expense_saved": (
            "Збережено!\n"
            "Тип: {label}\n"
            "Опис: {notes}\n"
            "Сума: {amount} {currency}{conv_note}"
        ),
        # stats
        "stats_no_car": "Спочатку налаштуйте бота: /start",
        "stats_no_expenses": "Витрат ще немає. Починайте з /fuel або /service.",
        "stats_km": "📍 Пробіг: {km:.0f} км (від {start:.0f} до {current:.0f})",
        "stats_expenses": "💰 Витрати (без купівлі): {total:.2f} {currency}",
        "stats_total": "💰 Разом з ціною купівлі: {total:.2f} {currency}",
        "stats_cost_per_km": "📊 Вартість кілометра: {cost:.4f} {currency}/км",
        "stats_categories": "📋 По категоріях:",
        "stats_category_line": "  {label}: {amount:.2f} {currency}",
        "stats_last_eff": "⛽ З останньої заправки: {eff:.2f} км/л ({l100:.1f} л/100км)",
        "stats_avg_eff": "⛽ Середній за весь час: {eff:.2f} км/л ({l100:.1f} л/100км)",
        "stats_sheet": "📄 Google Sheet: {url}",
    },

    "en": {
        # auth
        "no_access": "⛔ Access denied.",
        # setup
        "start_welcome": "Hi! Tracking expenses for {make} {model}.",
        "start_first_time": "Hi! Let's set up the tracker.\n\nCar make?",
        "setup_update": "Updating car info.\n\nMake?",
        "commands_menu": (
            "/fuel — fuel up\n"
            "/service — service/repair\n"
            "/insurance — insurance\n"
            "/tax — taxes/fees\n"
            "/parking — parking\n"
            "/other — other expenses\n"
            "/stats — statistics\n"
            "/setup — update car info"
        ),
        "ask_make": "Car make?",
        "ask_model": "Model?",
        "ask_year": "Year of manufacture?",
        "err_year": "Enter a valid year (e.g. 2023).",
        "ask_odo_start": "Odometer at purchase (km)?",
        "err_odo": "Enter a number, e.g.: 15000",
        "ask_purchase_price": "Purchase price ({currency})?",
        "err_price": "Enter an amount, e.g.: 85000",
        "ask_tank_size": "Tank size (litres)?",
        "err_tank_size": "Enter a valid volume, e.g.: 55",
        "setup_done": "Saved! {make} {model}, tank {tank}L.\n\nYou can now log expenses:",
        "cancelled": "Cancelled.",
        # fuel
        "ask_odo": "Current odometer (km)?",
        "err_odo_number": "Enter a number, e.g.: 15320",
        "ask_liters": "How many litres did you fill?",
        "err_liters": "Enter litres, e.g.: 42.5",
        "err_tank_overflow": "Warning: {liters}L exceeds tank size ({tank}L). Please check and re-enter.",
        "ask_full_tank": "Full tank?",
        "btn_full_yes": "Yes — full",
        "btn_full_no": "No — partial",
        "label_full": "full tank",
        "label_partial": "partial",
        "cat_fuel": "Fuel",
        "fuel_saved": (
            "Saved!\n"
            "Odometer: {odo} km\n"
            "Filled: {liters} L ({full_label})\n"
            "Paid: {amount} {currency}{conv_note}\n"
            "Price per litre: {price} {base_currency}/L"
        ),
        # amount input
        "amount_hint": "Amount in {base_currency}, or with currency code: «10 EUR», «500 CZK», «8.50 GBP»",
        "err_amount": "Didn't understand. {hint}",
        "err_unknown_currency": "Unknown currency «{code}». {hint}",
        # expense
        "ask_desc": "{label} — brief description?",
        "ask_odo_optional": "Current odometer (km)? Or /skip to skip.",
        "err_odo_or_skip": "Enter km or /skip.",
        "expense_saved": (
            "Saved!\n"
            "Type: {label}\n"
            "Description: {notes}\n"
            "Amount: {amount} {currency}{conv_note}"
        ),
        # stats
        "stats_no_car": "Set up the bot first: /start",
        "stats_no_expenses": "No expenses yet. Start with /fuel or /service.",
        "stats_km": "📍 Distance: {km:.0f} km (from {start:.0f} to {current:.0f})",
        "stats_expenses": "💰 Expenses (excl. purchase): {total:.2f} {currency}",
        "stats_total": "💰 Total incl. purchase price: {total:.2f} {currency}",
        "stats_cost_per_km": "📊 Cost per km: {cost:.4f} {currency}/km",
        "stats_categories": "📋 By category:",
        "stats_category_line": "  {label}: {amount:.2f} {currency}",
        "stats_last_eff": "⛽ Since last fill-up: {eff:.2f} km/L ({l100:.1f} L/100km)",
        "stats_avg_eff": "⛽ Lifetime average: {eff:.2f} km/L ({l100:.1f} L/100km)",
        "stats_sheet": "📄 Google Sheet: {url}",
    },

    "pl": {
        # auth
        "no_access": "⛔ Brak dostępu.",
        # setup
        "start_welcome": "Cześć! Śledzę wydatki dla {make} {model}.",
        "start_first_time": "Cześć! Skonfigurujmy tracker.\n\nMarka samochodu?",
        "setup_update": "Aktualizacja danych auta.\n\nMarka?",
        "commands_menu": (
            "/fuel — tankowanie\n"
            "/service — serwis/naprawa\n"
            "/insurance — ubezpieczenie\n"
            "/tax — podatki/opłaty\n"
            "/parking — parking\n"
            "/other — inne wydatki\n"
            "/stats — statystyki\n"
            "/setup — zmień dane auta"
        ),
        "ask_make": "Marka samochodu?",
        "ask_model": "Model?",
        "ask_year": "Rok produkcji?",
        "err_year": "Podaj poprawny rok (np. 2023).",
        "ask_odo_start": "Przebieg przy zakupie (km)?",
        "err_odo": "Podaj liczbę km, np.: 15000",
        "ask_purchase_price": "Cena zakupu ({currency})?",
        "err_price": "Podaj kwotę, np.: 85000",
        "ask_tank_size": "Pojemność baku (litry)?",
        "err_tank_size": "Podaj poprawną pojemność, np.: 55",
        "setup_done": "Zapisano! {make} {model}, bak {tank}l.\n\nMożesz teraz wprowadzać wydatki:",
        "cancelled": "Anulowano.",
        # fuel
        "ask_odo": "Aktualny przebieg (km)?",
        "err_odo_number": "Podaj liczbę, np.: 15320",
        "ask_liters": "Ile litrów zatankowałeś?",
        "err_liters": "Podaj litry, np.: 42.5",
        "err_tank_overflow": "Uwaga: {liters}l przekracza pojemność baku ({tank}l). Sprawdź i wpisz ponownie.",
        "ask_full_tank": "Pełny bak?",
        "btn_full_yes": "Tak — pełny",
        "btn_full_no": "Nie — częściowe",
        "label_full": "pełny bak",
        "label_partial": "częściowe",
        "cat_fuel": "Paliwo",
        "fuel_saved": (
            "Zapisano!\n"
            "Przebieg: {odo} km\n"
            "Zatankowano: {liters} l ({full_label})\n"
            "Zapłacono: {amount} {currency}{conv_note}\n"
            "Cena za litr: {price} {base_currency}/l"
        ),
        # amount input
        "amount_hint": "Kwota w {base_currency}, lub z kodem waluty: «10 EUR», «500 CZK», «8.50 GBP»",
        "err_amount": "Nie rozumiem. {hint}",
        "err_unknown_currency": "Nieznana waluta «{code}». {hint}",
        # expense
        "ask_desc": "{label} — krótki opis wydatku?",
        "ask_odo_optional": "Aktualny przebieg (km)? Lub /skip aby pominąć.",
        "err_odo_or_skip": "Podaj km lub /skip.",
        "expense_saved": (
            "Zapisano!\n"
            "Typ: {label}\n"
            "Opis: {notes}\n"
            "Kwota: {amount} {currency}{conv_note}"
        ),
        # stats
        "stats_no_car": "Najpierw skonfiguruj bota: /start",
        "stats_no_expenses": "Brak wydatków. Zacznij od /fuel lub /service.",
        "stats_km": "📍 Przebieg: {km:.0f} km (od {start:.0f} do {current:.0f})",
        "stats_expenses": "💰 Wydatki (bez zakupu): {total:.2f} {currency}",
        "stats_total": "💰 Razem z ceną zakupu: {total:.2f} {currency}",
        "stats_cost_per_km": "📊 Koszt kilometra: {cost:.4f} {currency}/km",
        "stats_categories": "📋 Według kategorii:",
        "stats_category_line": "  {label}: {amount:.2f} {currency}",
        "stats_last_eff": "⛽ Od ostatniego tankowania: {eff:.2f} km/l ({l100:.1f} l/100km)",
        "stats_avg_eff": "⛽ Średnia za cały okres: {eff:.2f} km/l ({l100:.1f} l/100km)",
        "stats_sheet": "📄 Google Sheet: {url}",
    },
}


def t(key: str, **kwargs) -> str:
    lang = LANGUAGE if LANGUAGE in _STRINGS else "en"
    template = _STRINGS[lang].get(key) or _STRINGS["en"].get(key, key)
    return template.format(**kwargs) if kwargs else template
