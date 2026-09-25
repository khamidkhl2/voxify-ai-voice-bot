from aiogram import Router
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from services.tts import VOICE_CATALOG

router = Router()

@router.inline_query()
async def inline_tts_handler(inline_query: InlineQuery):
    query = inline_query.query.strip()
    if not query:
        results = [
            InlineQueryResultArticle(
                id="hint",
                title="🗣 Type any text to generate AI Voice",
                description="Example: @YourBot Hello world, this is AI speech!",
                input_message_content=InputTextMessageContent(
                    message_text="💡 Use <b>@YourBot &lt;text&gt;</b> in any chat to speak with AI Voice!",
                    parse_mode="HTML"
                )
            )
        ]
        await inline_query.answer(results, cache_time=5, is_personal=True)
        return

    bot_info = await inline_query.bot.get_me()
    results = []

    # Featured voices for quick inline sharing
    featured_voices = [
        ("en", "🇺🇸 Christopher (US Male)", "en-US-ChristopherNeural"),
        ("ru", "🇷🇺 Dmitry (Russian Male)", "ru-RU-DmitryNeural"),
        ("uz", "🇺🇿 Sardor (Uzbek Male)", "uz-UZ-SardorNeural"),
        ("es", "🇪🇸 Álvaro (Spanish Male)", "es-ES-AlvaroNeural"),
    ]

    for idx, (lang, label, voice_name) in enumerate(featured_voices):
        text_preview = query if len(query) <= 50 else query[:50] + "..."
        results.append(
            InlineQueryResultArticle(
                id=f"voice_{idx}",
                title=label,
                description=f"Speak: \"{text_preview}\"",
                input_message_content=InputTextMessageContent(
                    message_text=(
                        f"🗣 <b>\"{query}\"</b>\n\n"
                        f"🎙 <i>Voice: {label}\n"
                        f"⚡️ Spoken via @{bot_info.username} (AI Text-to-Speech)</i>"
                    ),
                    parse_mode="HTML"
                )
            )
        )

    await inline_query.answer(results, cache_time=10, is_personal=True)
