import logging
from telegram import Update, BotCommand
from telegram.ext import ApplicationBuilder, TypeHandler, ContextTypes, ApplicationHandlerStop

from config import TELEGRAM_TOKEN, ALLOWED_USER_IDS
from handlers import setup, fuel, expense, stats
from i18n import t

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    level=logging.INFO,
)

_COMMANDS = [
    BotCommand("fuel",      "⛽ Fuel up"),
    BotCommand("service",   "🔧 Service / repair"),
    BotCommand("insurance", "📋 Insurance"),
    BotCommand("tax",       "🏛 Taxes / fees"),
    BotCommand("parking",   "🅿️ Parking"),
    BotCommand("other",     "💸 Other expenses"),
    BotCommand("stats",     "📊 Statistics"),
    BotCommand("setup",     "🚗 Update car info"),
    BotCommand("cancel",    "❌ Cancel"),
]


async def _auth_guard(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if user is None or user.id not in ALLOWED_USER_IDS:
        if update.effective_message:
            await update.effective_message.reply_text(t("no_access"))
        raise ApplicationHandlerStop


async def _set_commands(app) -> None:
    await app.bot.set_my_commands(_COMMANDS)


def main() -> None:
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).post_init(_set_commands).build()

    app.add_handler(TypeHandler(Update, _auth_guard), group=-1)
    app.add_handler(setup.build_handler())
    app.add_handler(fuel.build_handler())
    app.add_handler(expense.build_handler())
    app.add_handler(stats.build_handler())

    logging.info("Bot started, allowed users: %s", ALLOWED_USER_IDS)
    app.run_polling()


if __name__ == "__main__":
    import asyncio
    asyncio.set_event_loop(asyncio.new_event_loop())
    main()
