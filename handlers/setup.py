from datetime import date

from telegram import Update
from telegram.ext import (
    CommandHandler, ConversationHandler, MessageHandler, filters, ContextTypes
)

import sheets
import currency as cur
from i18n import t

(MAKE, MODEL, YEAR, ODO_START, PURCHASE_PRICE, TANK_SIZE) = range(6)


async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    info = sheets.get_car_info()
    if info:
        await update.message.reply_text(
            t("start_welcome", make=info.get("make", ""), model=info.get("model", ""))
            + "\n\n" + t("commands_menu")
        )
        return ConversationHandler.END

    await update.message.reply_text(t("start_first_time"))
    return MAKE


async def setup_command(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(t("setup_update"))
    return MAKE


async def get_make(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    ctx.user_data["make"] = update.message.text.strip()
    await update.message.reply_text(t("ask_model"))
    return MODEL


async def get_model(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    ctx.user_data["model"] = update.message.text.strip()
    await update.message.reply_text(t("ask_year"))
    return YEAR


async def get_year(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip()
    if not text.isdigit() or not (1900 < int(text) < 2100):
        await update.message.reply_text(t("err_year"))
        return YEAR
    ctx.user_data["year"] = text
    await update.message.reply_text(t("ask_odo_start"))
    return ODO_START


async def get_odo_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip().replace(" ", "").replace(",", "")
    if not text.isdigit():
        await update.message.reply_text(t("err_odo"))
        return ODO_START
    ctx.user_data["odometer_start_km"] = text
    await update.message.reply_text(t("ask_purchase_price", base_currency=cur.BASE_CURRENCY))
    return PURCHASE_PRICE


async def get_purchase_price(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    parsed = cur.parse_amount(update.message.text)
    if parsed is None:
        await update.message.reply_text(t("err_price"))
        return PURCHASE_PRICE
    amount, orig_currency = parsed
    if orig_currency != cur.BASE_CURRENCY and not await cur.is_valid(orig_currency):
        await update.message.reply_text(t("err_price"))
        return PURCHASE_PRICE
    ctx.user_data["purchase_price"] = str(amount)
    ctx.user_data["purchase_price_currency"] = orig_currency
    await update.message.reply_text(t("ask_tank_size"))
    return TANK_SIZE


async def get_tank_size(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip().replace(",", ".")
    try:
        val = float(text)
        if val <= 0 or val > 200:
            raise ValueError
    except ValueError:
        await update.message.reply_text(t("err_tank_size"))
        return TANK_SIZE

    ctx.user_data["tank_size_liters"] = text
    ctx.user_data["purchased_on"] = str(date.today())

    sheets.save_car_info(ctx.user_data)

    make = ctx.user_data["make"]
    model = ctx.user_data["model"]
    await update.message.reply_text(
        t("setup_done", make=make, model=model, tank=text) + "\n" + t("commands_menu")
    )
    return ConversationHandler.END


async def cancel(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(t("cancelled"))
    return ConversationHandler.END


def build_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            CommandHandler("setup", setup_command),
        ],
        states={
            MAKE:           [MessageHandler(filters.TEXT & ~filters.COMMAND, get_make)],
            MODEL:          [MessageHandler(filters.TEXT & ~filters.COMMAND, get_model)],
            YEAR:           [MessageHandler(filters.TEXT & ~filters.COMMAND, get_year)],
            ODO_START:      [MessageHandler(filters.TEXT & ~filters.COMMAND, get_odo_start)],
            PURCHASE_PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_purchase_price)],
            TANK_SIZE:      [MessageHandler(filters.TEXT & ~filters.COMMAND, get_tank_size)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
