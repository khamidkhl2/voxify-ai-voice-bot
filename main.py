import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import BotCommand

from config import config
from database.db import db

# Import routers
from handlers.start import router as start_router
from handlers.admin import router as admin_router
from handlers.voice_settings import router as voice_router
from handlers.sponsor_gate import router as sponsor_gate_router
from handlers.advertise import router as advertise_router
from handlers.inline_mode import router as inline_router
from handlers.tts_handler import router as tts_router

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
logger = logging.getLogger(__name__)

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Start bot & view stats"),
        BotCommand(command="voice", description="Select AI voices & languages"),
        BotCommand(command="lang", description="Switch interface language"),
        BotCommand(command="vip", description="Get Ad-Free VIP Pass (Stars)"),
        BotCommand(command="referral", description="Invite friends for free VIP"),
        BotCommand(command="advertise", description="Promote your channel"),
        BotCommand(command="help", description="How to use the bot"),
    ]
    await bot.set_my_commands(commands)

async def main():
    if not config.BOT_TOKEN:
        logger.error("BOT_TOKEN is not set in environment or .env file! Please configure it.")
        return

    # Initialize Database
    logger.info("Initializing database...")
    await db.init()

    # Initialize Bot & Dispatcher
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    # Register Routers in order of priority
    dp.include_router(admin_router)
    dp.include_router(start_router)
    dp.include_router(voice_router)
    dp.include_router(sponsor_gate_router)
    dp.include_router(advertise_router)
    dp.include_router(inline_router)
    # TTS text handler must be last
    dp.include_router(tts_router)

    # Set Telegram Menu Commands
    await set_commands(bot)

    bot_user = await bot.get_me()
    logger.info(f"Bot @{bot_user.username} is successfully running!")

    # Start Polling
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
