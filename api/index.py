import os
import sys
import json
import asyncio
import traceback
from http.server import BaseHTTPRequestHandler

# Lazy-loaded bot & dispatcher to prevent module import crashes on Vercel
_bot = None
_dp = None
_db_initialized = False

def get_bot():
    global _bot
    if _bot is None:
        from aiogram import Bot
        from aiogram.enums import ParseMode
        from aiogram.client.default import DefaultBotProperties
        from config import config

        token = config.BOT_TOKEN or os.getenv("BOT_TOKEN", "")
        if not token:
            raise ValueError("BOT_TOKEN is missing! Please add it in Vercel Project Settings -> Environment Variables.")
        
        _bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    return _bot

def get_dispatcher():
    global _dp
    if _dp is None:
        from aiogram import Dispatcher
        from handlers.start import router as start_router
        from handlers.admin import router as admin_router
        from handlers.voice_settings import router as voice_router
        from handlers.sponsor_gate import router as sponsor_gate_router
        from handlers.advertise import router as advertise_router
        from handlers.inline_mode import router as inline_router
        from handlers.tts_handler import router as tts_router

        _dp = Dispatcher()
        _dp.include_router(admin_router)
        _dp.include_router(start_router)
        _dp.include_router(voice_router)
        _dp.include_router(sponsor_gate_router)
        _dp.include_router(advertise_router)
        _dp.include_router(inline_router)
        _dp.include_router(tts_router)
    return _dp

async def init_services():
    global _db_initialized
    if not _db_initialized:
        from database.db import db
        await db.init()
        _db_initialized = True

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            host = self.headers.get("Host", "")
            path = self.path

            if "set_webhook" in path:
                bot = get_bot()
                webhook_url = f"https://{host}/"
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    res = loop.run_until_complete(bot.set_webhook(url=webhook_url))
                    info = loop.run_until_complete(bot.get_webhook_info())
                    msg = (
                        f"<h1>✅ Webhook Successfully Configured!</h1>"
                        f"<p><b>Target URL:</b> {webhook_url}</p>"
                        f"<p><b>Telegram Webhook URL:</b> {info.url}</p>"
                        f"<p><b>Pending Updates:</b> {info.pending_update_count}</p>"
                        f"<p>👉 Open Telegram and message your bot!</p>"
                    )
                finally:
                    loop.close()

                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(msg.encode("utf-8"))
                return

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            
            token_status = "Configured ✅" if (os.getenv("BOT_TOKEN")) else "Missing ❌ (Add BOT_TOKEN in Vercel Settings)"
            html = (
                f"<h2>🎙 Voxify AI Voice Bot is Live on Vercel!</h2>"
                f"<p><b>BOT_TOKEN Status:</b> {token_status}</p>"
                f"<p><a href='/set_webhook' style='padding: 8px 16px; background: #0070f3; color: white; text-decoration: none; border-radius: 5px;'>Click Here to Connect Webhook</a></p>"
            )
            self.wfile.write(html.encode("utf-8"))

        except Exception as e:
            tb = traceback.format_exc()
            self.send_response(200) # Send 200 so Vercel doesn't obscure it with a generic 500 error page
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.end_headers()
            err_msg = f"⚠️ Voxify Bot Error:\n\n{tb}"
            self.wfile.write(err_msg.encode("utf-8"))

    def do_POST(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)

            if not body:
                self.send_response(200)
                self.end_headers()
                return

            data = json.loads(body.decode("utf-8"))
            from aiogram.types import Update

            bot = get_bot()
            dp = get_dispatcher()

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
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"ok": false}')
