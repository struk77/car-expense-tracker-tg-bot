from datetime import date, timedelta

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

import sheets
from config import BASE_CURRENCY, EXPENSE_CATEGORIES, SPREADSHEET_ID
from i18n import t


async def cmd_stats(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    info = sheets.get_car_info()
    if not info:
        await update.message.reply_text(t("stats_no_car"))
        return

    expenses = sheets.get_all_expenses()
    if not expenses:
        await update.message.reply_text(t("stats_no_expenses"))
        return

    cutoff = str(date.today() - timedelta(days=30))
    recent = [r for r in expenses if r.get("date", "") >= cutoff]

    odo_start = float(info.get("odometer_start_km", 0))
    odometers = [float(r["odometer_km"]) for r in expenses if r.get("odometer_km")]
    current_odo = max(odometers) if odometers else odo_start
    km_driven = current_odo - odo_start

    total = sum(float(r["base_amount"]) for r in expenses if r.get("base_amount"))
    total_30d = sum(float(r["base_amount"]) for r in recent if r.get("base_amount"))
    cost_per_km = total / km_driven if km_driven > 0 else 0

    cost_per_km_dep = None
    purchase_price = float(info.get("purchase_price") or info.get("purchase_price_pln", 0))
    purchase_currency = info.get("purchase_price_currency", BASE_CURRENCY)
    purchased_on = info.get("purchased_on")
    if purchase_price and purchased_on and purchase_currency == BASE_CURRENCY and km_driven > 0:
        years = max(1.0, (date.today() - date.fromisoformat(purchased_on)).days / 365.25)
        depreciation = purchase_price * min(1.0, years * 0.1)
        cost_per_km_dep = (total + depreciation) / km_driven

    by_category: dict[str, float] = {}
    by_category_30d: dict[str, float] = {}
    for r in expenses:
        cat = r.get("category", "other")
        by_category[cat] = by_category.get(cat, 0) + float(r.get("base_amount") or 0)
    for r in recent:
        cat = r.get("category", "other")
        by_category_30d[cat] = by_category_30d.get(cat, 0) + float(r.get("base_amount") or 0)

    last_eff, avg_eff = _compute_efficiency(expenses)

    lines = [
        f"🚗 {info.get('make', '')} {info.get('model', '')} {info.get('year', '')}",
        "",
        t("stats_km", km=km_driven, start=odo_start, current=current_odo),
        "",
        t("stats_expenses", total=total, total_30d=total_30d, currency=BASE_CURRENCY),
        t("stats_cost_per_km", cost=cost_per_km, currency=BASE_CURRENCY),
    ]

    if cost_per_km_dep is not None:
        lines.append(t("stats_cost_per_km_dep", cost=cost_per_km_dep, currency=BASE_CURRENCY))

    lines += ["", t("stats_categories")]

    all_cats = {cat: t(f"cat_{cat}") for cat in ["fuel", *EXPENSE_CATEGORIES, "income"]}
    for cat, label in all_cats.items():
        amt = by_category.get(cat, 0)
        if amt:
            if cat == "income":
                amt = abs(amt)
            amt_30d = by_category_30d.get(cat, 0)
            if amt_30d:
                if cat == "income":
                    amt_30d = abs(amt_30d)
                lines.append(t("stats_category_line_30d", label=label, amount=amt, amount_30d=amt_30d, currency=BASE_CURRENCY))
            else:
                lines.append(t("stats_category_line", label=label, amount=amt, currency=BASE_CURRENCY))

    if last_eff:
        lines += ["", t("stats_last_eff", eff=last_eff, l100=100 / last_eff)]
    if avg_eff:
        lines.append(t("stats_avg_eff", eff=avg_eff, l100=100 / avg_eff))

    sheet_url = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}"
    lines += ["", t("stats_sheet", url=sheet_url)]

    await update.message.reply_text("\n".join(lines))


def _compute_efficiency(expenses: list[dict]) -> tuple[float | None, float | None]:
    fuel_rows = [r for r in expenses if r.get("category") == "fuel" and r.get("odometer_km")]
    fuel_rows.sort(key=lambda r: (r.get("date", ""), float(r["odometer_km"])))

    full_fills = [
        (float(r["odometer_km"]), float(r["liters"]))
        for r in fuel_rows
        if r.get("full_tank", "").upper() == "TRUE" and r.get("liters")
    ]

    if len(full_fills) < 2:
        return None, None

    efficiencies: list[float] = []
    for i in range(1, len(full_fills)):
        odo_prev, _ = full_fills[i - 1]
        odo_curr, _ = full_fills[i]
        km = odo_curr - odo_prev
        liters_between = sum(
            float(r["liters"])
            for r in fuel_rows
            if odo_prev < float(r["odometer_km"]) <= odo_curr and r.get("liters")
        )
        if km > 0 and liters_between > 0:
            efficiencies.append(km / liters_between)

    if not efficiencies:
        return None, None

    return efficiencies[-1], sum(efficiencies) / len(efficiencies)


def build_handler() -> CommandHandler:
    return CommandHandler("stats", cmd_stats)
