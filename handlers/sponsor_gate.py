from aiogram import Router, F
from aiogram.types import CallbackQuery, LabeledPrice
from services.sponsor_service import sponsor_service
from services.i18n import get_text
from database.db import db
from keyboards.inline import get_sponsor_keyboard
from config import config

router = Router()

@router.callback_query(F.data == "check_sponsor_subs")
async def callback_check_subs(callback: CallbackQuery):
    user_id = callback.from_user.id
    user = await db.get_user(user_id)
    lang = user.get("language", "en") if user else "en"

    is_passed, missing = await sponsor_service.verify_subscriptions(callback.bot, user_id)

    if is_passed:
        await callback.message.delete()
        await callback.message.answer(
            get_text("verify_success", lang),
            parse_mode="HTML"
        )
        await callback.answer("✅")
    else:
        kb = get_sponsor_keyboard(missing, lang=lang)
        await callback.message.edit_text(
            get_text("sponsor_gate", lang),
            reply_markup=kb,
            parse_mode="HTML"
        )
        await callback.answer(get_text("verify_fail", lang), show_alert=True)

@router.callback_query(F.data == "buy_vip_stars")
async def callback_buy_vip_stars(callback: CallbackQuery):
    prices = [LabeledPrice(label="VIP Pass (30 Days)", amount=config.VIP_PRICE_STARS)]
    await callback.bot.send_invoice(
        chat_id=callback.message.chat.id,
        title="⭐ 30-Day VIP Pass",
        description="Bypass all sponsor channels, get priority audio rendering, and ad-free experience.",
        payload=f"vip_{callback.from_user.id}",
        currency="XTR",
        prices=prices
    )
    await callback.answer()
