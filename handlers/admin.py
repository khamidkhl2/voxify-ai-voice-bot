import asyncio
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from database.db import db
from config import config

router = Router()

def is_admin(user_id: int) -> bool:
    return user_id in config.ADMIN_IDS if config.ADMIN_IDS else False

@router.message(Command("admin"))
async def cmd_admin(message: Message):
    if not is_admin(message.from_user.id):
        return

    stats = await db.get_stats()
    text = (
        "👑 <b>Admin Control Panel</b>\n\n"
        f"👥 <b>Total Users:</b> {stats['total_users']}\n"
        f"⭐ <b>VIP Users:</b> {stats['total_vips']}\n"
        f"📢 <b>Active Sponsors:</b> {stats['active_sponsors']}\n"
        f"🎯 <b>Delivered Subscribers:</b> {stats['delivered_subs']}\n\n"
        "<b>Available Admin Commands:</b>\n"
        "• <code>/add_sponsor &lt;chat_id&gt; &lt;invite_link&gt; &lt;target_subs&gt; &lt;Title&gt;</code>\n"
        "• <code>/sponsors</code> - View and remove active sponsor channels\n"
        "• <code>/broadcast &lt;text&gt;</code> - Send mass message to all users\n"
        "• <code>/give_vip &lt;user_id&gt; &lt;days&gt;</code> - Grant VIP to a user\n"
    )
    await message.answer(text, parse_mode="HTML")

@router.message(Command("add_sponsor"))
async def cmd_add_sponsor(message: Message):
    if not is_admin(message.from_user.id):
        return

    # /add_sponsor @mychannel https://t.me/+xyz 1000 My Channel Name
    parts = message.text.split(maxsplit=4)
    if len(parts) < 5:
        await message.answer(
            "⚠️ <b>Usage:</b>\n"
            "<code>/add_sponsor &lt;channel_id_or_username&gt; &lt;invite_link&gt; &lt;target_subs&gt; &lt;Title&gt;</code>\n\n"
            "Example:\n<code>/add_sponsor @daily_ai https://t.me/daily_ai 500 Daily AI News</code>",
            parse_mode="HTML"
        )
        return

    channel_id = parts[1]
    invite_link = parts[2]
    try:
        target_subs = int(parts[3])
    except ValueError:
        await message.answer("Target subs must be an integer!")
        return
    title = parts[4]

    sponsor_id = await db.add_sponsor(
        channel_id=channel_id,
        title=title,
        invite_link=invite_link,
        target_subs=target_subs,
        owner_id=message.from_user.id
    )

    await message.answer(
        f"✅ <b>Sponsor #{sponsor_id} Added!</b>\n\n"
        f"📢 <b>Title:</b> {title}\n"
        f"🆔 <b>Channel:</b> {channel_id}\n"
        f"🔗 <b>Link:</b> {invite_link}\n"
        f"🎯 <b>Target:</b> {target_subs} subs\n\n"
        "<i>Note: Make sure the bot is an Administrator in this channel so it can verify memberships!</i>",
        parse_mode="HTML"
    )

@router.message(Command("sponsors"))
async def cmd_list_sponsors(message: Message):
    if not is_admin(message.from_user.id):
        return

    sponsors = await db.get_active_sponsors()
    if not sponsors:
        await message.answer("ℹ️ No active sponsor channels right now.")
        return

    for s in sponsors:
        text = (
            f"📢 <b>{s['title']}</b> (ID: {s['id']})\n"
            f"Channel: <code>{s['channel_id']}</code>\n"
            f"Link: {s['invite_link']}\n"
            f"Progress: <b>{s['delivered_subs']} / {s['target_subs']}</b> subs"
        )
        del_kb = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="🗑 Delete Sponsor", callback_data=f"del_sponsor:{s['id']}")
        ]])
        await message.answer(text, reply_markup=del_kb, parse_mode="HTML")

@router.callback_query(F.data.startswith("del_sponsor:"))
async def callback_delete_sponsor(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        return
    sponsor_id = int(callback.data.split(":", 1)[1])
    await db.remove_sponsor(sponsor_id)
    await callback.message.edit_text("🗑 Sponsor channel removed from rotation.")
    await callback.answer("Deleted!")

@router.message(Command("give_vip"))
async def cmd_give_vip(message: Message):
    if not is_admin(message.from_user.id):
        return
    parts = message.text.split()
    if len(parts) < 2:
        await message.answer("Usage: <code>/give_vip &lt;user_id&gt; [days]</code>", parse_mode="HTML")
        return
    try:
        target_user = int(parts[1])
        days = int(parts[2]) if len(parts) > 2 else 30
        await db.set_vip(target_user, days)
        await message.answer(f"✅ Granted {days} days of VIP to user {target_user}!")
    except Exception as e:
        await message.answer(f"Error: {e}")

@router.message(Command("broadcast"))
async def cmd_broadcast(message: Message):
    if not is_admin(message.from_user.id):
        return

    text_to_broadcast = message.text[len("/broadcast"):].strip()
    if not text_to_broadcast:
        await message.answer("Usage: <code>/broadcast &lt;Your HTML Message&gt;</code>", parse_mode="HTML")
        return

    status_msg = await message.answer("🚀 Starting mass broadcast...")
    
    # Broadcast to all users in DB
    import aiosqlite
    from database.db import DB_PATH
    
    sent = 0
    failed = 0
    async with aiosqlite.connect(DB_PATH) as conn:
        cursor = await conn.execute("SELECT user_id FROM users")
        rows = await cursor.fetchall()

    for row in rows:
        uid = row[0]
        try:
            await message.bot.send_message(chat_id=uid, text=text_to_broadcast, parse_mode="HTML")
            sent += 1
            await asyncio.sleep(0.05) # Rate limit protection (20-30 msg/sec)
        except Exception:
            failed += 1

    await status_msg.edit_text(
        f"✅ <b>Broadcast Complete!</b>\n\n"
        f"• Successfully sent: {sent}\n"
        f"• Failed/Blocked: {failed}",
        parse_mode="HTML"
    )
