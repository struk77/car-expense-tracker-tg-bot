from datetime import date

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackQueryHandler, CommandHandler, ConversationHandler,
    MessageHandler, filters, ContextTypes,
)

import sheets
import currency as cur
from i18n import t

(ODO, LITERS, FULL_TANK, AMOUNT) = range(4)


async def cmd_fuel(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(t("ask_odo"))
    return ODO


async def get_odo(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip().replace(" ", "").replace(",", "")
    if not text.isdigit():
        await update.message.reply_text(t("err_odo_number"))
        return ODO
    ctx.user_data["odo"] = int(text)
    await update.message.reply_text(t("ask_liters"))
    return LITERS


async def get_liters(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip().replace(",", ".")
    try:
        liters = float(text)
        if liters <= 0:
            raise ValueError
    except ValueError:
        await update.message.reply_text(t("err_liters"))
        return LITERS

    info = sheets.get_car_info() or {}
    tank_size = float(info.get("tank_size_liters", 999))
    if liters > tank_size:
        await update.message.reply_text(t("err_tank_overflow", liters=liters, tank=tank_size))
        return LITERS

    ctx.user_data["liters"] = liters
    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton(t("btn_full_yes"), callback_data="full_yes"),
        InlineKeyboardButton(t("btn_full_no"), callback_data="full_no"),
    ]])
    await update.message.reply_text(t("ask_full_tank"), reply_markup=kb)
    return FULL_TANK


async def get_full_tank(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    ctx.user_data["full_tank"] = query.data == "full_yes"
    await query.edit_message_text(t("amount_hint", base_currency=cur.BASE_CURRENCY))
    return AMOUNT


async def get_amount(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    parsed = cur.parse_amount(update.message.text)
    hint = t("amount_hint", base_currency=cur.BASE_CURRENCY)
    if parsed is None:
        await update.message.reply_text(t("err_amount", hint=hint))
        return AMOUNT

    amount, orig_currency = parsed
    if orig_currency != cur.BASE_CURRENCY and not await cur.is_valid(orig_currency):
        await update.message.reply_text(t("err_unknown_currency", code=orig_currency, hint=hint))
        return AMOUNT

    liters = ctx.user_data["liters"]
    base_amount = await cur.to_base(amount, orig_currency)
    price_per_liter = round(base_amount / liters, 4) if liters else 0

    row = {
        "date": str(date.today()),
        "category": "fuel",
        "odometer_km": ctx.user_data["odo"],
        "liters": liters,
        "full_tank": "TRUE" if ctx.user_data["full_tank"] else "FALSE",
        "currency": orig_currency,
        "original_amount": amount,
        "base_amount": base_amount,
        "price_per_liter_base": price_per_liter,
        "notes": "",
        "entered_by": update.effective_user.full_name,
    }
    sheets.add_expense(row)

    full_label = t("label_full") if ctx.user_data["full_tank"] else t("label_partial")
    conv_note = f" ({base_amount:.2f} {cur.BASE_CURRENCY})" if orig_currency != cur.BASE_CURRENCY else ""
    await update.message.reply_text(t(
        "fuel_saved",
        odo=ctx.user_data["odo"],
        liters=liters,
        full_label=full_label,
        amount=amount,
        currency=orig_currency,
        conv_note=conv_note,
        price=price_per_liter,
        base_currency=cur.BASE_CURRENCY,
    ))
    return ConversationHandler.END


async def cancel(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(t("cancelled"))
    return ConversationHandler.END


def build_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[CommandHandler("fuel", cmd_fuel)],
        states={
            ODO:       [MessageHandler(filters.TEXT & ~filters.COMMAND, get_odo)],
            LITERS:    [MessageHandler(filters.TEXT & ~filters.COMMAND, get_liters)],
            FULL_TANK: [CallbackQueryHandler(get_full_tank, pattern="^full_")],
            AMOUNT:    [MessageHandler(filters.TEXT & ~filters.COMMAND, get_amount)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        per_message=False,
    )
