from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

import sheets
from config import BASE_CURRENCY, CATEGORIES, SPREADSHEET_ID
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

    odo_start = float(info.get("odometer_start_km", 0))
    purchase_price = float(info.get("purchase_price_pln", 0))

    odometers = [float(r["odometer_km"]) for r in expenses if r.get("odometer_km")]
    current_odo = max(odometers) if odometers else odo_start
    km_driven = current_odo - odo_start

    total = sum(float(r["pln_amount"]) for r in expenses if r.get("pln_amount"))
    total_with_purchase = total + purchase_price
    cost_per_km = (total_with_purchase / km_driven) if km_driven > 0 else 0

    by_category: dict[str, float] = {}
    for r in expenses:
        cat = r.get("category", "other")
        by_category[cat] = by_category.get(cat, 0) + float(r.get("pln_amount") or 0)

    last_eff, avg_eff = _compute_efficiency(expenses)

    lines = [
        f"🚗 {info.get('make', '')} {info.get('model', '')} {info.get('year', '')}",
        "",
        t("stats_km", km=km_driven, start=odo_start, current=current_odo),
        "",
        t("stats_expenses", total=total, currency=BASE_CURRENCY),
        t("stats_total", total=total_with_purchase, currency=BASE_CURRENCY),
        t("stats_cost_per_km", cost=cost_per_km, currency=BASE_CURRENCY),
        "",
        t("stats_categories"),
    ]

    all_cats = {"fuel": t("cat_fuel"), **CATEGORIES}
    for cat, label in all_cats.items():
        amt = by_category.get(cat, 0)
        if amt:
            lines.append(t("stats_category_line", label=label, amount=amt, currency=BASE_CURRENCY))

    if last_eff:
        lines += ["", t("stats_last_eff", eff=last_eff, l100=100 / last_eff)]
    if avg_eff:
        lines.append(t("stats_avg_eff", eff=avg_eff, l100=100 / avg_eff))

    sheet_url = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}"
    lines += ["", t("stats_sheet", url=sheet_url)]

    await update.message.reply_text("\n".join(lines))


def _compute_efficiency(expenses: list[dict]) -> tuple[float | None, float | None]:
    fuel_rows = [r for r in expenses if r.get("category") == "fuel"]
    fuel_rows.sort(key=lambda r: (r.get("date", ""), float(r.get("odometer_km") or 0)))

    full_fills = [
        (float(r["odometer_km"]), float(r["liters"]))
        for r in fuel_rows
        if r.get("full_tank", "").upper() == "TRUE"
        and r.get("odometer_km") and r.get("liters")
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
            if r.get("odometer_km")
            and odo_prev < float(r["odometer_km"]) <= odo_curr
            and r.get("liters")
        )
        if km > 0 and liters_between > 0:
            efficiencies.append(km / liters_between)

    if not efficiencies:
        return None, None

    return efficiencies[-1], sum(efficiencies) / len(efficiencies)


def build_handler() -> CommandHandler:
    return CommandHandler("stats", cmd_stats)
