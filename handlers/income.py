from datetime import date

from telegram import Update
from telegram.ext import (
    CommandHandler, ConversationHandler,
    MessageHandler, filters, ContextTypes,
)

import sheets
import currency as cur
from i18n import t

(DESC, AMOUNT) = range(2)


async def cmd_income(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(t("ask_income_desc"))
    return DESC


async def get_desc(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    ctx.user_data["income_notes"] = update.message.text.strip()
    await update.message.reply_text(t("amount_hint", base_currency=cur.BASE_CURRENCY))
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

    base_amount = await cur.to_base(amount, orig_currency)
    latest_odo = sheets.get_latest_odometer() or ""

    row = {
        "date": str(date.today()),
        "category": "income",
        "odometer_km": latest_odo,
        "liters": "",
        "full_tank": "",
        "currency": orig_currency,
        "original_amount": amount,
        "base_amount": -base_amount,
        "price_per_liter_base": "",
        "notes": ctx.user_data.get("income_notes", ""),
        "entered_by": update.effective_user.full_name,
    }
    sheets.add_expense(row)

    conv_note = f" ({base_amount:.2f} {cur.BASE_CURRENCY})" if orig_currency != cur.BASE_CURRENCY else ""
    await update.message.reply_text(t("income_saved", amount=amount, currency=orig_currency, conv_note=conv_note))
    return ConversationHandler.END


async def cancel(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(t("cancelled"))
    return ConversationHandler.END


def build_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[CommandHandler("income", cmd_income)],
        states={
            DESC:   [MessageHandler(filters.TEXT & ~filters.COMMAND, get_desc)],
            AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_amount)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        per_message=False,
    )
