import os
from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.enums import ChatAction
from database.db import db
from services.sponsor_service import sponsor_service
from services.tts import tts_service
from services.i18n import get_text
from keyboards.inline import get_sponsor_keyboard, get_audio_share_keyboard
from config import config

router = Router()

@router.message(F.text & ~F.text.startswith("/"))
@router.edited_message(F.text & ~F.text.startswith("/"))
async def handle_tts_request(message: Message):
    user_id = message.from_user.id
    text = message.text.strip()
    
    user = await db.get_user(user_id)
    if not user:
        user = await db.get_or_create_user(
            user_id=user_id,
            username=message.from_user.username or "",
            first_name=message.from_user.first_name or "",
            tg_lang=message.from_user.language_code or "en"
        )
    lang = user.get("language", "en") if user else "en"

    # 1. Sponsor Gating Check
    is_passed, missing_sponsors = await sponsor_service.verify_subscriptions(message.bot, user_id)
    if not is_passed:
        kb = get_sponsor_keyboard(missing_sponsors, lang=lang)
        await message.answer(
            get_text("sponsor_gate", lang),
            reply_markup=kb,
            parse_mode="HTML"
        )
        return

    # 2. Length validation
    is_vip = await db.is_user_vip(user_id)
    max_len = 3000 if is_vip else 1000
    if len(text) > max_len:
        await message.answer(
            get_text("too_long", lang, max_len=max_len),
            parse_mode="HTML"
        )
        return

    # 3. Processing notification
    bot_info = await message.bot.get_me()
    await message.bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.RECORD_VOICE)

    voice = user.get("selected_voice", "auto") if user else "auto"
    fmt = user.get("format", "voice") if user else "voice"
    as_voice_note = (fmt == "voice")

    status_msg = await message.answer(get_text("generating", lang), parse_mode="HTML")

    try:
        audio_path = await tts_service.generate_speech(
            text=text,
            voice=voice,
            as_voice_note=as_voice_note
        )

        # 4. Ad banner & attribution
        ad_line = ""
        if not is_vip:
            ad_line = f"\n\n📢 <i>{config.FALLBACK_AD_TEXT}</i>"

        caption = f"🎙 <b>Voice:</b> <code>{voice}</code>{ad_line}"
        reply_kb = get_audio_share_keyboard(bot_info.username, lang=lang)

        input_file = FSInputFile(audio_path)
        if as_voice_note and audio_path.endswith(".ogg"):
            await message.answer_voice(
                voice=input_file,
                caption=caption,
                reply_markup=reply_kb,
                parse_mode="HTML"
            )
        else:
            await message.answer_audio(
                audio=input_file,
                caption=caption,
                title="AI TTS Audio",
                performer=f"@{bot_info.username}",
                reply_markup=reply_kb,
                parse_mode="HTML"
            )

        if os.path.exists(audio_path):
            os.remove(audio_path)

        await status_msg.delete()

    except Exception as e:
        print(f"Error during TTS generation: {e}")
        await status_msg.edit_text(
            get_text("error_gen", lang),
            parse_mode="HTML"
        )
