from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery
from database.db import db
from keyboards.inline import get_language_keyboard
from services.i18n import get_text
from config import config

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username or ""
    first_name = message.from_user.first_name or "Friend"
    tg_lang = message.from_user.language_code or "en"
    
    args = message.text.split()[1] if len(message.text.split()) > 1 else ""
    referrer_id = None
    if args.startswith("ref_") and args[4:].isdigit():
        referrer_id = int(args[4:])

    user = await db.get_or_create_user(user_id, username, first_name, tg_lang=tg_lang, referrer_id=referrer_id)
    lang = user.get("language", "en")

    welcome_text = get_text(
        "welcome", 
        lang, 
        name=first_name, 
        voice=user.get("selected_voice", "auto"),
        format=user.get("format", "voice")
    )

    await message.answer(welcome_text, parse_mode="HTML")

@router.message(Command("help"))
async def cmd_help(message: Message):
    user = await db.get_user(message.from_user.id)
    lang = user.get("language", "en") if user else "en"
    await message.answer(get_text("help", lang), parse_mode="HTML")

@router.message(Command("lang"))
async def cmd_lang(message: Message):
    user = await db.get_user(message.from_user.id)
    lang = user.get("language", "en") if user else "en"
    await message.answer(get_text("select_lang", lang), reply_markup=get_language_keyboard(), parse_mode="HTML")

@router.callback_query(F.data == "open_lang")
async def callback_open_lang(callback: CallbackQuery):
    user = await db.get_user(callback.from_user.id)
    lang = user.get("language", "en") if user else "en"
    await callback.message.edit_text(get_text("select_lang", lang), reply_markup=get_language_keyboard(), parse_mode="HTML")
    await callback.answer()

@router.callback_query(F.data.startswith("set_ui_lang:"))
async def callback_set_ui_lang(callback: CallbackQuery):
    lang_code = callback.data.split(":", 1)[1]
    await db.update_user_language(callback.from_user.id, lang_code)
    await callback.message.edit_text(get_text("lang_changed", lang_code), parse_mode="HTML")
    await callback.answer("Saved!")

@router.message(Command("referral"))
async def cmd_referral(message: Message):
    user = await db.get_user(message.from_user.id)
    bot_info = await message.bot.get_me()
    ref_link = f"https://t.me/{bot_info.username}?start=ref_{message.from_user.id}"
    ref_count = user["referral_count"] if user else 0

    text = (
        "👥 <b>Invite Friends — Get Free VIP!</b>\n\n"
        f"Your personal referral link:\n<code>{ref_link}</code>\n\n"
        f"📊 <b>Invited Friends:</b> {ref_count} / {config.REFERRALS_FOR_VIP}\n\n"
        f"🎁 <i>Invite {config.REFERRALS_FOR_VIP} friends to get <b>1 Month of VIP</b> completely free (bypasses all ads & sponsor checks)!</i>"
    )
    await message.answer(text, parse_mode="HTML")

@router.message(Command("vip"))
async def cmd_vip(message: Message):
    is_vip = await db.is_user_vip(message.from_user.id)
    if is_vip:
        await message.answer("⭐ <b>You are already a VIP Member!</b>\nAll ads and sponsor requirements are disabled for you.", parse_mode="HTML")
        return

    prices = [LabeledPrice(label="VIP Pass (30 Days)", amount=config.VIP_PRICE_STARS)]
    await message.bot.send_invoice(
        chat_id=message.chat.id,
        title="⭐ 30-Day VIP Pass",
        description="Bypass all sponsor channels, get priority audio rendering, and ad-free experience.",
        payload=f"vip_{message.from_user.id}",
        currency="XTR",
        prices=prices
    )

@router.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)

@router.message(F.successful_payment)
async def process_successful_payment(message: Message):
    payload = message.successful_payment.invoice_payload
    if payload.startswith("vip_"):
        user_id = int(payload.split("_")[1])
        await db.set_vip(user_id, days=30)
        await message.answer("🎉 <b>Thank you! Your 30-day VIP Pass is now ACTIVE.</b>\nYou now enjoy ad-free unlimited AI TTS.", parse_mode="HTML")
