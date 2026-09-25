import os
import json
import asyncio
from http.server import BaseHTTPRequestHandler
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Update

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

# Singleton Bot & Dispatcher initialized once per Lambda container
bot = Bot(
    token=config.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()
dp.include_router(admin_router)
dp.include_router(start_router)
dp.include_router(voice_router)
dp.include_router(sponsor_gate_router)
dp.include_router(advertise_router)
dp.include_router(inline_router)
dp.include_router(tts_router)

_db_initialized = False

async def init_services():
    global _db_initialized
    if not _db_initialized:
        await db.init()
        _db_initialized = True

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        host = self.headers.get("Host", "")
        path = self.path

        if "/set_webhook" in path:
            webhook_url = f"https://{host}/"
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                res = loop.run_until_complete(bot.set_webhook(url=webhook_url))
                info = loop.run_until_complete(bot.get_webhook_info())
                msg = f"✅ Webhook successfully set to {webhook_url}!\nTelegram status: {info.url}"
            except Exception as e:
                msg = f"❌ Error setting webhook: {e}"
            finally:
                loop.close()

            self.send_response(200)
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(msg.encode("utf-8"))
            return

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        html = (
            "<h2>🎙 Voxify AI Voice Bot is Live on Vercel!</h2>"
            "<p>To configure Telegram webhook, visit: <a href='/set_webhook'>/set_webhook</a></p>"
        )
        self.wfile.write(html.encode("utf-8"))

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        if not body:
            self.send_response(400)
            self.end_headers()
            return

        try:
            data = json.loads(body.decode("utf-8"))
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(init_services())
                update = Update.model_validate(data, context={"bot": bot})
                loop.run_until_complete(dp.feed_update(bot=bot, update=update))
            finally:
                loop.close()

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"ok": true}')
        except Exception as e:
            print(f"Error handling webhook update: {e}")
            self.send_response(500)
            self.end_headers()
