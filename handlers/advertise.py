from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database.db import db
from services.crypto_pay import crypto_pay
from keyboards.inline import get_advertising_keyboard
from config import config

router = Router()

class AdOrderStates(StatesGroup):
    waiting_for_channel_info = State()

@router.message(Command("advertise"))
@router.message(Command("sponsor"))
async def cmd_advertise(message: Message):
    text = (
        "📈 <b>Promote Your Channel via AI TTS Bot</b>\n\n"
        "Get guaranteed, active Telegram subscribers through our <b>Mandatory Subscription (ОП)</b> engine!\n\n"
        "⚡️ <b>How it works:</b>\n"
        "1. Every user must join your channel to unlock free AI voice generations.\n"
        "2. The bot automatically tracks delivered subscribers.\n"
        "3. Real-time activation via CryptoPay (USDT, TON, BTC) or direct admin contact.\n\n"
        "👇 <b>Select a package to start:</b>"
    )
    await message.answer(text, reply_markup=get_advertising_keyboard(), parse_mode="HTML")

@router.callback_query(F.data == "open_advertise")
async def callback_open_advertise(callback: CallbackQuery):
    await cmd_advertise(callback.message)
    await callback.answer()

@router.callback_query(F.data.startswith("buy_sponsor:"))
async def callback_buy_sponsor(callback: CallbackQuery, state: FSMContext):
    tier_id = callback.data.split(":", 1)[1]
    tier = config.SPONSOR_TIERS.get(tier_id)
    if not tier:
        await callback.answer("Package not found", show_alert=True)
        return

    await state.update_data(tier_id=tier_id, subs=tier["subs"], price_usd=tier["price_usd"])
    await state.set_state(AdOrderStates.waiting_for_channel_info)

    await callback.message.answer(
        f"📝 <b>You selected: {tier['subs']} Subscribers (${tier['price_usd']} USD)</b>\n\n"
        "Please reply with your Channel details in this format:\n"
        "<code>@YourChannelUsername https://t.me/your_invite_link Channel Title</code>\n\n"
        "<i>Make sure you add our bot as an Administrator in your channel so it can verify subscribers!</i>",
        parse_mode="HTML"
    )
    await callback.answer()

@router.message(AdOrderStates.waiting_for_channel_info)
async def process_channel_info(message: Message, state: FSMContext):
    parts = message.text.strip().split(maxsplit=2)
    if len(parts) < 3:
        await message.answer(
            "⚠️ Invalid format. Please send: <code>@Username InviteLink ChannelTitle</code>\n"
            "Example: <code>@tech_news https://t.me/+AbCdEf Tech News Today</code>",
            parse_mode="HTML"
        )
        return

    channel_username = parts[0]
    invite_link = parts[1]
    channel_title = parts[2]
    
    data = await state.get_data()
    subs = data["subs"]
    price_usd = data["price_usd"]
    user_id = message.from_user.id

    if crypto_pay.is_configured():
        # Create CryptoPay invoice
        desc = f"Sponsor placement: {subs} subs for {channel_title}"
        invoice = await crypto_pay.create_invoice(
            amount_usd=price_usd,
            description=desc,
            payload=f"ad_{user_id}_{subs}"
        )

        if invoice:
            await db.create_invoice_record(
                invoice_id=invoice["invoice_id"],
                user_id=user_id,
                channel_id=channel_username,
                channel_title=channel_title,
                invite_link=invite_link,
                target_subs=subs,
                amount_usd=price_usd,
                pay_url=invoice["pay_url"]
            )

            pay_kb = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=f"💳 Pay ${price_usd} via CryptoBot", url=invoice["pay_url"])],
                [InlineKeyboardButton(text="🔄 Check Payment", callback_data=f"check_invoice:{invoice['invoice_id']}")]
            ])

            await message.answer(
                f"✅ <b>Invoice Created!</b>\n\n"
                f"📢 <b>Channel:</b> {channel_title} ({channel_username})\n"
                f"🎯 <b>Target Subscribers:</b> {subs}\n"
                f"💰 <b>Total Price:</b> ${price_usd} USD\n\n"
                f"Click the button below to pay via <b>@CryptoBot</b> (supports USDT, TON, BTC). "
                f"Your sponsor slot will activate automatically once payment is detected!",
                reply_markup=pay_kb,
                parse_mode="HTML"
            )
            await state.clear()
            return

    # If CryptoPay is not configured or fails, alert admin
    await db.add_sponsor(
        channel_id=channel_username,
        title=channel_title,
        invite_link=invite_link,
        target_subs=subs,
        owner_id=user_id,
        channel_username=channel_username
    )
    await message.answer(
        "✅ <b>Order Placed!</b>\n"
        f"Your channel <b>{channel_title}</b> has been queued for {subs} subscribers.\n"
        "An admin will verify the listing.",
        parse_mode="HTML"
    )
    await state.clear()

@router.callback_query(F.data.startswith("check_invoice:"))
async def callback_check_invoice(callback: CallbackQuery):
    invoice_id = callback.data.split(":", 1)[1]
    status = await crypto_pay.check_invoice_status(invoice_id)

    if status == "paid":
        inv = await db.mark_invoice_paid(invoice_id)
        if inv:
            await callback.message.edit_text(
                "🎉 <b>Payment Confirmed!</b>\n\n"
                f"Your channel <b>{inv['channel_title']}</b> is now active in the bot's sponsor rotation! "
                f"Subscribers will now be directed to your channel.",
                parse_mode="HTML"
            )
        else:
            await callback.answer("Channel is already active!", show_alert=True)
    elif status == "active":
        await callback.answer("Payment still pending. Please complete payment in @CryptoBot first.", show_alert=True)
    else:
        await callback.answer(f"Status: {status or 'Unknown'}. Try again in a moment.", show_alert=True)
