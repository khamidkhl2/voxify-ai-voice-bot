from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List, Dict, Any
from services.tts import VOICE_CATALOG
from services.i18n import get_text
from config import config

def get_language_keyboard() -> InlineKeyboardMarkup:
    """Keyboard for selecting bot interface language"""
    buttons = [
        [
            InlineKeyboardButton(text="🇺🇸 English", callback_data="set_ui_lang:en"),
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="set_ui_lang:ru"),
        ],
        [
            InlineKeyboardButton(text="🇪🇸 Español", callback_data="set_ui_lang:es"),
            InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="set_ui_lang:uz"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_voice_categories_keyboard(current_voice: str) -> InlineKeyboardMarkup:
    """Top-level voice menu: Auto-detect + Language categories"""
    buttons = []
    
    # Auto detect button
    auto_check = "✅ " if current_voice == "auto" else ""
    buttons.append([
        InlineKeyboardButton(text=f"{auto_check}🤖 Auto-Detect Language (Smart)", callback_data="set_voice:auto")
    ])

    # Languages row by row (2 per row)
    row = []
    for lang_code, data in VOICE_CATALOG.items():
        row.append(InlineKeyboardButton(text=data["label"], callback_data=f"voice_cat:{lang_code}"))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)

    buttons.append([
        InlineKeyboardButton(text="⚙️ Audio Format (Voice / MP3)", callback_data="open_settings"),
        InlineKeyboardButton(text="🌐 Interface Language", callback_data="open_lang")
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_voices_for_category_keyboard(lang_code: str, current_voice: str) -> InlineKeyboardMarkup:
    """Shows specific voices for a selected language"""
    data = VOICE_CATALOG.get(lang_code)
    buttons = []
    if data:
        for v in data["voices"]:
            is_sel = "✅ " if v["id"] == current_voice else ""
            buttons.append([
                InlineKeyboardButton(text=f"{is_sel}{v['name']}", callback_data=f"set_voice:{v['id']}")
            ])

    buttons.append([
        InlineKeyboardButton(text="🔙 Back to Languages", callback_data="open_voices")
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_sponsor_keyboard(missing_sponsors: List[Dict[str, Any]], lang: str = "en") -> InlineKeyboardMarkup:
    buttons = []
    for i, sponsor in enumerate(missing_sponsors, 1):
        buttons.append([
            InlineKeyboardButton(text=f"📢 {i}. Join {sponsor['title']}", url=sponsor['invite_link'])
        ])

    buttons.append([
        InlineKeyboardButton(text=get_text("btn_verify", lang), callback_data="check_sponsor_subs")
    ])
    buttons.append([
        InlineKeyboardButton(text=f"{get_text('btn_vip', lang)} ({config.VIP_PRICE_STARS} ⭐)", callback_data="buy_vip_stars")
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_settings_keyboard(current_format: str) -> InlineKeyboardMarkup:
    voice_check = "✅ " if current_format == "voice" else ""
    audio_check = "✅ " if current_format == "audio" else ""
    
    buttons = [
        [
            InlineKeyboardButton(text=f"{voice_check}🎙 Voice Note (Waveform)", callback_data="set_format:voice"),
            InlineKeyboardButton(text=f"{audio_check}🎵 MP3 Audio File", callback_data="set_format:audio"),
        ],
        [
            InlineKeyboardButton(text="🔙 Back to Voices", callback_data="open_voices")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_audio_share_keyboard(bot_username: str, lang: str = "en") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text=get_text("btn_share", lang), 
                url=f"https://t.me/{bot_username}?start=ref"
            )
        ],
        [
            InlineKeyboardButton(
                text=get_text("btn_ad", lang), 
                callback_data="open_advertise"
            )
        ]
    ])

def get_advertising_keyboard() -> InlineKeyboardMarkup:
    buttons = []
    for tier_id, tier in config.SPONSOR_TIERS.items():
        text = f"🚀 {tier['subs']} Subscribers - ${tier['price_usd']} USD"
        buttons.append([
            InlineKeyboardButton(text=text, callback_data=f"buy_sponsor:{tier_id}")
        ])
    
    buttons.append([
        InlineKeyboardButton(text="💬 Contact Admin", url="https://t.me/CryptoBot")
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
