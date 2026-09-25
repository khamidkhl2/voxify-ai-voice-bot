from typing import Dict, Any

MESSAGES: Dict[str, Dict[str, str]] = {
    "en": {
        "welcome": (
            "👋 <b>Welcome, {name}!</b>\n\n"
            "I am an ultra-realistic <b>AI Text-to-Speech (TTS) Bot</b>. "
            "Send me any text, and I will instantly voice it using neural AI!\n\n"
            "🎙 <b>Current Voice:</b> <code>{voice}</code>\n"
            "📁 <b>Audio Format:</b> <code>{format}</code>\n"
            "🌐 <b>Bot Language:</b> 🇺🇸 English\n\n"
            "🔹 <i>To change voice & language:</i> /voice\n"
            "🔹 <i>To switch bot interface language:</i> /lang\n"
            "🔹 <i>To invite friends for free VIP:</i> /referral\n"
            "🔹 <i>To remove all ads (VIP):</i> /vip\n"
            "🔹 <i>To promote your channel:</i> /advertise\n\n"
            "👉 <b>Just send me any text now to hear it!</b>"
        ),
        "help": (
            "📖 <b>How to use AI TTS Bot:</b>\n\n"
            "1. Simply send any text in any language.\n"
            "2. The bot will automatically speak it in high-definition audio.\n"
            "3. Switch languages and accents using /voice.\n"
            "4. Switch between Telegram Voice Notes and MP3 files in /voice settings.\n\n"
            "🌟 <b>Commands:</b>\n"
            "/voice - Select AI voices & languages\n"
            "/lang - Switch interface language\n"
            "/vip - Get Ad-Free VIP Pass with Telegram Stars\n"
            "/referral - Invite friends & get free VIP\n"
            "/advertise - Promote your channel to bot users"
        ),
        "sponsor_gate": (
            "🔒 <b>To use the free AI Text-to-Speech, please subscribe to our sponsors:</b>\n\n"
            "This keeps our servers running 100% free for everyone! "
            "Subscribe to the channels below, then tap <b>Verify</b> to unlock instant voice generation:"
        ),
        "verify_success": "🎉 <b>Subscription Verified!</b>\n\nSend me any text now and I will voice it for you!",
        "verify_fail": "❌ You haven't joined all required channels yet. Please subscribe to all sponsors above.",
        "generating": "⚡️ <i>Generating AI speech...</i>",
        "too_long": "⚠️ <b>Text too long!</b> Maximum allowed is {max_len} characters.",
        "error_gen": "❌ <b>Error generating audio.</b> Please try again or switch voice with /voice.",
        "btn_verify": "🔄 I've Subscribed (Verify)",
        "btn_vip": "⭐ Skip Ads with VIP",
        "btn_share": "🗣 Voice your own text (Free)",
        "btn_ad": "📢 Advertise Here",
        "select_lang": "🌐 <b>Select Bot Language:</b>",
        "lang_changed": "✅ Language changed to English!"
    },
    "ru": {
        "welcome": (
            "👋 <b>Добро пожаловать, {name}!</b>\n\n"
            "Я бот для озвучки текста с помощью <b>нейросетей (AI TTS)</b>. "
            "Отправь мне любой текст, и я мгновенно озвучу его живым реалистичным голосом!\n\n"
            "🎙 <b>Текущий голос:</b> <code>{voice}</code>\n"
            "📁 <b>Формат аудио:</b> <code>{format}</code>\n"
            "🌐 <b>Язык интерфейса:</b> 🇷🇺 Русский\n\n"
            "🔹 <i>Выбрать голос и язык:</i> /voice\n"
            "🔹 <i>Сменить язык бота:</i> /lang\n"
            "🔹 <i>Пригласить друзей (бесплатный VIP):</i> /referral\n"
            "🔹 <i>Отключить рекламу (VIP):</i> /vip\n"
            "🔹 <i>Купить рекламу канала:</i> /advertise\n\n"
            "👉 <b>Просто отправь мне текст, чтобы озвучить его!</b>"
        ),
        "help": (
            "📖 <b>Как пользоваться ботом:</b>\n\n"
            "1. Отправь любой текст на любом языке.\n"
            "2. Бот мгновенно сгенерирует голосовое сообщение с реалистичной интонацией.\n"
            "3. Выбирай мужские и женские голоса в /voice.\n"
            "4. Переключай между голосовыми сообщениями и MP3 файлами в /voice.\n\n"
            "🌟 <b>Команды:</b>\n"
            "/voice - Выбор голоса и формата\n"
            "/lang - Сменить язык бота\n"
            "/vip - Отключить рекламу через Telegram Stars\n"
            "/referral - Реферальная программа\n"
            "/advertise - Разместить рекламу своего канала"
        ),
        "sponsor_gate": (
            "🔒 <b>Чтобы бесплатно пользоваться озвучкой, подпишитесь на наших спонсоров:</b>\n\n"
            "Это позволяет нашему сервису оставаться бесплатным! "
            "Подпишитесь на каналы ниже и нажмите <b>Проверить</b>:"
        ),
        "verify_success": "🎉 <b>Подписка подтверждена!</b>\n\nОтправьте любой текст для озвучки!",
        "verify_fail": "❌ Вы еще не подписались на все каналы. Пожалуйста, подпишитесь на спонсоров выше.",
        "generating": "⚡️ <i>Генерирую голос...</i>",
        "too_long": "⚠️ <b>Текст слишком длинный!</b> Максимум {max_len} символов.",
        "error_gen": "❌ <b>Ошибка генерации.</b> Попробуйте другой текст или смените голос в /voice.",
        "btn_verify": "🔄 Я подписался (Проверить)",
        "btn_vip": "⭐ Отключить рекламу (VIP)",
        "btn_share": "🗣 Озвучить свой текст бесплатно",
        "btn_ad": "📢 Купить рекламу",
        "select_lang": "🌐 <b>Выберите язык интерфейса:</b>",
        "lang_changed": "✅ Язык переключен на русский!"
    },
    "es": {
        "welcome": (
            "👋 <b>¡Bienvenido, {name}!</b>\n\n"
            "Soy un bot de <b>Texto a Voz con IA (TTS)</b> ultra realista. "
            "¡Envíame cualquier texto y lo convertiré en audio con voces neuronales!\n\n"
            "🎙 <b>Voz actual:</b> <code>{voice}</code>\n"
            "📁 <b>Formato:</b> <code>{format}</code>\n"
            "🌐 <b>Idioma:</b> 🇪🇸 Español\n\n"
            "🔹 <i>Cambiar voz e idioma:</i> /voice\n"
            "🔹 <i>Cambiar idioma de la interfaz:</i> /lang\n"
            "🔹 <i>Invitar amigos (VIP gratis):</i> /referral\n"
            "🔹 <i>Quitar anuncios (VIP):</i> /vip\n"
            "🔹 <i>Promocionar tu canal:</i> /advertise\n\n"
            "👉 <b>¡Envíame cualquier texto ahora para escucharlo!</b>"
        ),
        "help": (
            "📖 <b>Cómo usar el bot:</b>\n\n"
            "1. Envía cualquier texto en cualquier idioma.\n"
            "2. El bot generará audio realista en alta definición.\n"
            "3. Cambia voces y acentos con /voice.\n\n"
            "🌟 <b>Comandos:</b>\n"
            "/voice - Cambiar voces\n"
            "/lang - Cambiar idioma\n"
            "/vip - Quitar anuncios\n"
            "/referral - Invitar amigos\n"
            "/advertise - Promocionar canal"
        ),
        "sponsor_gate": (
            "🔒 <b>Para usar la voz con IA gratis, suscríbete a nuestros patrocinadores:</b>\n\n"
            "Suscríbete a los canales a continuación y toca <b>Verificar</b>:"
        ),
        "verify_success": "🎉 <b>¡Suscripción verificada!</b>\n\n¡Envíame cualquier texto ahora!",
        "verify_fail": "❌ Aún no te has suscrito a todos los canales requeridos.",
        "generating": "⚡️ <i>Generando voz con IA...</i>",
        "too_long": "⚠️ <b>Texto demasiado largo.</b>",
        "error_gen": "❌ Error al generar audio. Intenta de nuevo.",
        "btn_verify": "🔄 Ya me suscribí (Verificar)",
        "btn_vip": "⭐ Omitir anuncios con VIP",
        "btn_share": "🗣 Crea tu propio audio gratis",
        "btn_ad": "📢 Publicidad aquí",
        "select_lang": "🌐 <b>Selecciona el idioma del bot:</b>",
        "lang_changed": "✅ ¡Idioma cambiado a español!"
    },
    "uz": {
        "welcome": (
            "👋 <b>Xush kelibsiz, {name}!</b>\n\n"
            "Men matnni jonli ovozga aylantiruvchi <b>AI Ovoz (TTS) Botiman</b>. "
            "Menga istalgan matn yuboring va men uni sun'iy intellekt orqali ovozga aylantirib beraman!\n\n"
            "🎙 <b>Joriy ovoz:</b> <code>{voice}</code>\n"
            "📁 <b>Audio formati:</b> <code>{format}</code>\n"
            "🌐 <b>Bot tili:</b> 🇺🇿 O'zbekcha\n\n"
            "🔹 <i>Ovoz va tilni tanlash:</i> /voice\n"
            "🔹 <i>Bot interfeysi tilini o'zgartirish:</i> /lang\n"
            "🔹 <i>Do'stlarni taklif qilish (bepul VIP):</i> /referral\n"
            "🔹 <i>Reklamasiz VIP olish:</i> /vip\n"
            "🔹 <i>Kanalni reklama qilish:</i> /advertise\n\n"
            "👉 <b>Hoziroq matn yuboring va eshitib ko'ring!</b>"
        ),
        "help": (
            "📖 <b>Botdan foydalanish bo'yicha qo'llanma:</b>\n\n"
            "1. Istalgan tilda matn yuboring.\n"
            "2. Bot uni yuqori sifatli ovozli xabarga aylantiradi.\n"
            "3. /voice orqali ovozlarni o'zgartirishingiz mumkin.\n\n"
            "🌟 <b>Buyruqlar:</b>\n"
            "/voice - Ovozlar va sozlamalar\n"
            "/lang - Bot tilini o'zgartirish\n"
            "/vip - Reklamasiz VIP olish\n"
            "/referral - Do'stlarni taklif qilish\n"
            "/advertise - Reklama berish"
        ),
        "sponsor_gate": (
            "🔒 <b>Bepul ovozdan foydalanish uchun homiy kanallarga obuna bo'ling:</b>\n\n"
            "Quyidagi kanallarga a'zo bo'ling va <b>Tekshirish</b> tugmasini bosing:"
        ),
        "verify_success": "🎉 <b>Obuna tasdiqlandi!</b>\n\nIstalgan matnni yuboring!",
        "verify_fail": "❌ Siz hali barcha homiy kanallarga a'zo bo'lmadingiz.",
        "generating": "⚡️ <i>Ovoz yaratilmoqda...</i>",
        "too_long": "⚠️ <b>Matn juda uzun!</b>",
        "error_gen": "❌ Ovoz yaratishda xatolik yuz berdi.",
        "btn_verify": "🔄 A'zo bo'ldim (Tekshirish)",
        "btn_vip": "⭐ Reklamasiz VIP olish",
        "btn_share": "🗣 O'z matningizni bepul ovoz qiling",
        "btn_ad": "📢 Reklama berish",
        "select_lang": "🌐 <b>Bot tilini tanlang:</b>",
        "lang_changed": "✅ Bot tili o'zbekchaga o'zgartirildi!"
    }
}

def get_text(key: str, lang: str = "en", **kwargs) -> str:
    lang_dict = MESSAGES.get(lang, MESSAGES["en"])
    text_template = lang_dict.get(key, MESSAGES["en"].get(key, key))
    if kwargs:
        return text_template.format(**kwargs)
    return text_template
