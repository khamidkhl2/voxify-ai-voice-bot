import aiosqlite
import os
import time
from typing import Optional, List, Dict, Any

# On Vercel serverless, /tmp is the only writable directory
DEFAULT_DB = "/tmp/bot_data.db" if os.getenv("VERCEL") else os.path.join(os.path.dirname(__file__), "bot_data.db")
DB_PATH = os.getenv("DB_PATH", DEFAULT_DB)

class Database:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    async def init(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    language TEXT DEFAULT 'en', -- 'en', 'ru', 'es', 'uz'
                    is_vip INTEGER DEFAULT 0,
                    vip_until INTEGER DEFAULT 0,
                    referrer_id INTEGER DEFAULT NULL,
                    referral_count INTEGER DEFAULT 0,
                    selected_voice TEXT DEFAULT 'auto', -- 'auto' or voice id
                    selected_rate TEXT DEFAULT '+0%',
                    selected_pitch TEXT DEFAULT '+0Hz',
                    format TEXT DEFAULT 'voice', -- 'voice' or 'audio'
                    created_at INTEGER
                )
            """)

            # Add language column if migrating existing db
            try:
                await db.execute("ALTER TABLE users ADD COLUMN language TEXT DEFAULT 'en'")
            except Exception:
                pass

            await db.execute("""
                CREATE TABLE IF NOT EXISTS sponsors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    channel_id TEXT NOT NULL,
                    channel_username TEXT,
                    title TEXT NOT NULL,
                    invite_link TEXT NOT NULL,
                    target_subs INTEGER NOT NULL,
                    delivered_subs INTEGER DEFAULT 0,
                    is_active INTEGER DEFAULT 1,
                    owner_id INTEGER DEFAULT 0,
                    created_at INTEGER
                )
            """)

            await db.execute("""
                CREATE TABLE IF NOT EXISTS user_sponsor_history (
                    user_id INTEGER,
                    sponsor_id INTEGER,
                    verified_at INTEGER,
                    PRIMARY KEY(user_id, sponsor_id)
                )
            """)

            await db.execute("""
                CREATE TABLE IF NOT EXISTS invoices (
                    invoice_id TEXT PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    channel_id TEXT NOT NULL,
                    channel_title TEXT NOT NULL,
                    invite_link TEXT NOT NULL,
                    target_subs INTEGER NOT NULL,
                    amount_usd REAL NOT NULL,
                    pay_url TEXT,
                    status TEXT DEFAULT 'pending',
                    created_at INTEGER
                )
            """)

            await db.commit()

    async def get_or_create_user(self, user_id: int, username: str, first_name: str, tg_lang: str = "en", referrer_id: Optional[int] = None) -> Dict[str, Any]:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            user = await cursor.fetchone()
            now = int(time.time())

            # Detect initial language
            detected_lang = "en"
            if tg_lang:
                tg_lower = tg_lang.lower()
                if "ru" in tg_lower:
                    detected_lang = "ru"
                elif "es" in tg_lower:
                    detected_lang = "es"
                elif "uz" in tg_lower:
                    detected_lang = "uz"

            if not user:
                ref_id = referrer_id if (referrer_id and referrer_id != user_id) else None
                await db.execute("""
                    INSERT INTO users (user_id, username, first_name, language, referrer_id, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (user_id, username, first_name, detected_lang, ref_id, now))
                
                if ref_id:
                    await db.execute("UPDATE users SET referral_count = referral_count + 1 WHERE user_id = ?", (ref_id,))
                    ref_cur = await db.execute("SELECT referral_count, is_vip, vip_until FROM users WHERE user_id = ?", (ref_id,))
                    referrer = await ref_cur.fetchone()
                    if referrer and referrer["referral_count"] >= 3:
                        new_vip_until = max(referrer["vip_until"], now) + 30 * 86400
                        await db.execute("UPDATE users SET is_vip = 1, vip_until = ? WHERE user_id = ?", (new_vip_until, ref_id))

                await db.commit()
                cursor = await db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
                user = await cursor.fetchone()

            return dict(user)

    async def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            row = await cursor.fetchone()
            return dict(row) if row else None

    async def update_user_language(self, user_id: int, language: str):
        now = int(time.time())
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO users (user_id, language, created_at)
                VALUES (?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET language = excluded.language
            """, (user_id, language, now))
            await db.commit()

    async def update_user_voice(self, user_id: int, voice: str):
        now = int(time.time())
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO users (user_id, selected_voice, created_at)
                VALUES (?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET selected_voice = excluded.selected_voice
            """, (user_id, voice, now))
            await db.commit()

    async def update_user_format(self, user_id: int, format_type: str):
        now = int(time.time())
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO users (user_id, format, created_at)
                VALUES (?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET format = excluded.format
            """, (user_id, format_type, now))
            await db.commit()

    async def set_vip(self, user_id: int, days: int = 30):
        now = int(time.time())
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cur = await db.execute("SELECT vip_until FROM users WHERE user_id = ?", (user_id,))
            row = await cur.fetchone()
            current_vip = row["vip_until"] if row and row["vip_until"] else now
            new_vip_until = max(current_vip, now) + (days * 86400)
            await db.execute("UPDATE users SET is_vip = 1, vip_until = ? WHERE user_id = ?", (new_vip_until, user_id))
            await db.commit()

    async def is_user_vip(self, user_id: int) -> bool:
        user = await self.get_user(user_id)
        if not user:
            return False
        if user["is_vip"] and user["vip_until"] > int(time.time()):
            return True
        return False

    async def get_active_sponsors(self) -> List[Dict[str, Any]]:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cursor = await db.execute("SELECT * FROM sponsors WHERE is_active = 1")
            rows = await cursor.fetchall()
            return [dict(r) for r in rows]

    async def add_sponsor(self, channel_id: str, title: str, invite_link: str, target_subs: int, owner_id: int = 0, channel_username: str = "") -> int:
        now = int(time.time())
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("""
                INSERT INTO sponsors (channel_id, channel_username, title, invite_link, target_subs, is_active, owner_id, created_at)
                VALUES (?, ?, ?, ?, ?, 1, ?, ?)
            """, (channel_id, channel_username, title, invite_link, target_subs, owner_id, now))
            await db.commit()
            return cursor.lastrowid

    async def record_sponsor_verification(self, user_id: int, sponsor_id: int):
        now = int(time.time())
        async with aiosqlite.connect(self.db_path) as db:
            try:
                await db.execute("""
                    INSERT INTO user_sponsor_history (user_id, sponsor_id, verified_at)
                    VALUES (?, ?, ?)
                """, (user_id, sponsor_id, now))
                await db.execute("""
                    UPDATE sponsors 
                    SET delivered_subs = delivered_subs + 1 
                    WHERE id = ?
                """, (sponsor_id,))
                
                cur = await db.execute("SELECT target_subs, delivered_subs FROM sponsors WHERE id = ?", (sponsor_id,))
                row = await cur.fetchone()
                if row and row[1] >= row[0]:
                    await db.execute("UPDATE sponsors SET is_active = 0 WHERE id = ?", (sponsor_id,))
                await db.commit()
            except aiosqlite.IntegrityError:
                pass

    async def remove_sponsor(self, sponsor_id: int):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("DELETE FROM sponsors WHERE id = ?", (sponsor_id,))
            await db.commit()

    async def get_stats(self) -> Dict[str, Any]:
        async with aiosqlite.connect(self.db_path) as db:
            u_cur = await db.execute("SELECT COUNT(*) FROM users")
            total_users = (await u_cur.fetchone())[0]

            vip_cur = await db.execute("SELECT COUNT(*) FROM users WHERE is_vip = 1 AND vip_until > ?", (int(time.time()),))
            total_vips = (await vip_cur.fetchone())[0]

            s_cur = await db.execute("SELECT COUNT(*) FROM sponsors WHERE is_active = 1")
            active_sponsors = (await s_cur.fetchone())[0]

            del_cur = await db.execute("SELECT SUM(delivered_subs) FROM sponsors")
            delivered_subs = (await del_cur.fetchone())[0] or 0

            return {
                "total_users": total_users,
                "total_vips": total_vips,
                "active_sponsors": active_sponsors,
                "delivered_subs": delivered_subs
            }

    async def create_invoice_record(self, invoice_id: str, user_id: int, channel_id: str, channel_title: str, invite_link: str, target_subs: int, amount_usd: float, pay_url: str):
        now = int(time.time())
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO invoices (invoice_id, user_id, channel_id, channel_title, invite_link, target_subs, amount_usd, pay_url, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'pending', ?)
            """, (invoice_id, user_id, channel_id, channel_title, invite_link, target_subs, amount_usd, pay_url, now))
            await db.commit()

    async def mark_invoice_paid(self, invoice_id: str) -> Optional[Dict[str, Any]]:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            cur = await db.execute("SELECT * FROM invoices WHERE invoice_id = ?", (invoice_id,))
            inv = await cur.fetchone()
            if inv and inv["status"] != "paid":
                await db.execute("UPDATE invoices SET status = 'paid' WHERE invoice_id = ?", (invoice_id,))
                await db.execute("""
                    INSERT INTO sponsors (channel_id, title, invite_link, target_subs, is_active, owner_id, created_at)
                    VALUES (?, ?, ?, ?, 1, ?, ?)
                """, (inv["channel_id"], inv["channel_title"], inv["invite_link"], inv["target_subs"], inv["user_id"], int(time.time())))
                await db.commit()
                return dict(inv)
            return None

db = Database()
