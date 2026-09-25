from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from database.db import db
from keyboards.inline import (
    get_voice_categories_keyboard, 
    get_voices_for_category_keyboard, 
    get_settings_keyboard
)

router = Router()

@router.message(Command("voice"))
async def cmd_voice(message: Message):
    user = await db.get_user(message.from_user.id)
    cur_voice = user.get("selected_voice", "auto") if user else "auto"
    kb = get_voice_categories_keyboard(cur_voice)
    await message.answer(
        "🎙 <b>AI Voice & Language Catalog:</b>\n\n"
        "Choose <b>Auto-Detect</b> (detects language automatically) or select a specific language below:",
        reply_markup=kb, 
        parse_mode="HTML"
    )

@router.callback_query(F.data == "open_voices")
async def callback_open_voices(callback: CallbackQuery):
    user = await db.get_user(callback.from_user.id)
    cur_voice = user.get("selected_voice", "auto") if user else "auto"
    kb = get_voice_categories_keyboard(cur_voice)
    await callback.message.edit_text(
        "🎙 <b>AI Voice & Language Catalog:</b>\n\n"
        "Choose <b>Auto-Detect</b> or select a language category below:",
        reply_markup=kb, 
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data.startswith("voice_cat:"))
async def callback_voice_category(callback: CallbackQuery):
    lang_code = callback.data.split(":", 1)[1]
    user = await db.get_user(callback.from_user.id)
    cur_voice = user.get("selected_voice", "auto") if user else "auto"
    kb = get_voices_for_category_keyboard(lang_code, cur_voice)
    await callback.message.edit_text(
        "🗣 <b>Choose a Voice:</b>\nSelect your preferred speaker:",
        reply_markup=kb,
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data.startswith("set_voice:"))
async def callback_set_voice(callback: CallbackQuery):
    voice_name = callback.data.split(":", 1)[1]
    await db.update_user_voice(callback.from_user.id, voice_name)
    label = "🤖 Auto-Detect Language" if voice_name == "auto" else voice_name
    await callback.message.edit_text(
        f"✅ <b>Voice updated!</b>\nSelected: <code>{label}</code>\n\nNow send any text to hear it speak!",
        parse_mode="HTML"
    )
    await callback.answer(f"Selected: {label}")

@router.callback_query(F.data == "open_settings")
async def callback_open_settings(callback: CallbackQuery):
    user = await db.get_user(callback.from_user.id)
    cur_format = user.get("format", "voice") if user else "voice"
    kb = get_settings_keyboard(cur_format)
    await callback.message.edit_text(
        "⚙️ <b>Audio Format Settings:</b>\n"
        "Choose whether the bot sends a native Telegram Voice Note with waveform or a standard MP3 file:",
        reply_markup=kb, 
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data.startswith("set_format:"))
async def callback_set_format(callback: CallbackQuery):
    fmt = callback.data.split(":", 1)[1]
    await db.update_user_format(callback.from_user.id, fmt)
    kb = get_settings_keyboard(fmt)
    await callback.message.edit_reply_markup(reply_markup=kb)
    await callback.answer(f"Format set to: {fmt}")
