from datetime import date

from telegram import Update
from telegram.ext import (
    CommandHandler, ConversationHandler,
    MessageHandler, filters, ContextTypes,
)

import sheets
import currency as cur
from i18n import t

(DESC, AMOUNT, ODO) = range(3)


async def _start(update: Update, ctx: ContextTypes.DEFAULT_TYPE, category: str) -> int:
    ctx.user_data["expense_category"] = category
    await update.message.reply_text(t("ask_desc", label=t(f"cat_{category}")))
    return DESC


async def cmd_service(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    return await _start(update, ctx, "service")


async def cmd_insurance(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    return await _start(update, ctx, "insurance")


async def cmd_tax(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    return await _start(update, ctx, "tax")


async def cmd_parking(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    return await _start(update, ctx, "parking")


async def cmd_other(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    return await _start(update, ctx, "other")


async def get_desc(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    ctx.user_data["expense_notes"] = update.message.text.strip()
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

    ctx.user_data["expense_amount"] = amount
    ctx.user_data["expense_currency"] = orig_currency
    await update.message.reply_text(t("ask_odo_optional"))
    return ODO


async def get_odo(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.strip().replace(" ", "").replace(",", "")
    if not text.isdigit():
        await update.message.reply_text(t("err_odo_or_skip"))
        return ODO
    ctx.user_data["expense_odo"] = int(text)
    return await _save(update, ctx)


async def skip_odo(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    ctx.user_data["expense_odo"] = ""
    return await _save(update, ctx)


async def _save(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    orig_currency = ctx.user_data["expense_currency"]
    amount = ctx.user_data["expense_amount"]
    base_amount = await cur.to_base(amount, orig_currency)

    row = {
        "date": str(date.today()),
        "category": ctx.user_data["expense_category"],
        "odometer_km": ctx.user_data.get("expense_odo", ""),
        "liters": "",
        "full_tank": "",
        "currency": orig_currency,
        "original_amount": amount,
        "base_amount": base_amount,
        "price_per_liter_base": "",
        "notes": ctx.user_data.get("expense_notes", ""),
        "entered_by": update.effective_user.full_name,
    }
    sheets.add_expense(row)

    label = t(f"cat_{ctx.user_data['expense_category']}")
    conv_note = f" ({base_amount:.2f} {cur.BASE_CURRENCY})" if orig_currency != cur.BASE_CURRENCY else ""
    await update.message.reply_text(t(
        "expense_saved",
        label=label,
        notes=ctx.user_data.get("expense_notes", "—"),
        amount=amount,
        currency=orig_currency,
        conv_note=conv_note,
    ))
    return ConversationHandler.END


async def cancel(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(t("cancelled"))
    return ConversationHandler.END


def build_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[
            CommandHandler("service", cmd_service),
            CommandHandler("insurance", cmd_insurance),
            CommandHandler("tax", cmd_tax),
            CommandHandler("parking", cmd_parking),
            CommandHandler("other", cmd_other),
        ],
        states={
            DESC:   [MessageHandler(filters.TEXT & ~filters.COMMAND, get_desc)],
            AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_amount)],
            ODO: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_odo),
                CommandHandler("skip", skip_odo),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        per_message=False,
    )
