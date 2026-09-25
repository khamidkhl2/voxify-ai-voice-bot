import os
import re
import asyncio
import edge_tts
import aiohttp
from typing import Optional, Dict, List, Any
from config import config

# Curated catalog of high quality neural voices grouped by language
VOICE_CATALOG: Dict[str, Dict[str, Any]] = {
    "en": {
        "label": "🇺🇸 English",
        "voices": [
            {"id": "en-US-ChristopherNeural", "name": "Christopher (US Male - Deep/Pro)"},
            {"id": "en-US-JennyNeural", "name": "Jenny (US Female - Natural)"},
            {"id": "en-US-GuyNeural", "name": "Guy (US Male - Casual)"},
            {"id": "en-GB-RyanNeural", "name": "Ryan (UK Male - British)"},
            {"id": "en-GB-SoniaNeural", "name": "Sonia (UK Female - British)"},
        ]
    },
    "ru": {
        "label": "🇷🇺 Русский",
        "voices": [
            {"id": "ru-RU-DmitryNeural", "name": "Дмитрий (Мужской)"},
            {"id": "ru-RU-SvetlanaNeural", "name": "Светлана (Женский)"},
        ]
    },
    "uz": {
        "label": "🇺🇿 O'zbekcha",
        "voices": [
            {"id": "uz-UZ-SardorNeural", "name": "Sardor (Erkak)"},
            {"id": "uz-UZ-MadinaNeural", "name": "Madina (Ayol)"},
        ]
    },
    "es": {
        "label": "🇪🇸 Español",
        "voices": [
            {"id": "es-ES-AlvaroNeural", "name": "Álvaro (España - Hombre)"},
            {"id": "es-MX-DaliaNeural", "name": "Dalia (México - Mujer)"},
        ]
    },
    "de": {
        "label": "🇩🇪 Deutsch",
        "voices": [
            {"id": "de-DE-ConradNeural", "name": "Conrad (Männlich)"},
            {"id": "de-DE-KatjaNeural", "name": "Katja (Weiblich)"},
        ]
    },
    "fr": {
        "label": "🇫🇷 Français",
        "voices": [
            {"id": "fr-FR-HenriNeural", "name": "Henri (Homme)"},
            {"id": "fr-FR-DeniseNeural", "name": "Denise (Femme)"},
        ]
    },
    "tr": {
        "label": "🇹🇷 Türkçe",
        "voices": [
            {"id": "tr-TR-AhmetNeural", "name": "Ahmet (Erkek)"},
            {"id": "tr-TR-EmelNeural", "name": "Emel (Kadın)"},
        ]
    },
    "ar": {
        "label": "🇸🇦 العربية",
        "voices": [
            {"id": "ar-SA-HamedNeural", "name": "حامد (رجالي)"},
            {"id": "ar-SA-ZariyahNeural", "name": "زارية (نسائي)"},
        ]
    },
    "pt": {
        "label": "🇧🇷 Português",
        "voices": [
            {"id": "pt-BR-AntonioNeural", "name": "Antônio (Masculino)"},
            {"id": "pt-BR-FranciscaNeural", "name": "Francisca (Feminino)"},
        ]
    },
    "hi": {
        "label": "🇮🇳 हिन्दी",
        "voices": [
            {"id": "hi-IN-MadhurNeural", "name": "Madhur (Male)"},
            {"id": "hi-IN-SwaraNeural", "name": "Swara (Female)"},
        ]
    }
}

class TTSService:
    @staticmethod
    def detect_auto_voice(text: str, default_voice: str = "en-US-ChristopherNeural") -> str:
        """
        Detects language family from text scripts and chooses best suited voice
        """
        # Arabic script check
        if re.search(r'[\u0600-\u06FF]', text):
            return "ar-SA-HamedNeural"
        
        # Devanagari (Hindi) check
        if re.search(r'[\u0900-\u097F]', text):
            return "hi-IN-MadhurNeural"

        # Cyrillic script check (Russian / Uzbek Cyrillic)
        if re.search(r'[а-яА-ЯёЁ]', text):
            # Check for specific Uzbek Cyrillic letters
            if re.search(r'[ғқҳўҒҚҲЎ]', text):
                return "uz-UZ-SardorNeural"
            return "ru-RU-DmitryNeural"

        # Check for Uzbek Latin unique characters and common stems
        if re.search(r"[oO]['`ʻ’][gG]['`ʻ’]", text) or re.search(r"\b(salom|alaykum|qanday|rahmat|yaxshi|uchun|kerak|emas|boladi|bormi|boshqa|mening|bizning)\w*", text, re.IGNORECASE):
            return "uz-UZ-SardorNeural"

        # Check for Spanish accents/inverted marks
        if re.search(r'[¿¡áéíóúñÁÉÍÓÚÑ]', text):
            return "es-ES-AlvaroNeural"

        # Check for German umlauts
        if re.search(r'[äöüßÄÖÜ]', text):
            return "de-DE-ConradNeural"

        # Check for French accents
        if re.search(r'[àâçéèêëîïôûùüÿœæÀÂÇÉÈÊËÎÏÔÛÙÜŸŒÆ]', text):
            return "fr-FR-HenriNeural"

        # Check for Turkish unique letters
        if re.search(r'[ğışçöüĞİŞÇÖÜ]', text):
            return "tr-TR-AhmetNeural"

        return default_voice

    @staticmethod
    async def convert_mp3_to_ogg(mp3_path: str, ogg_path: str) -> bool:
        try:
            cmd = [
                "ffmpeg", "-y", "-i", mp3_path,
                "-c:a", "libopus", "-b:a", "32k",
                "-vbr", "on", "-compression_level", "10",
                ogg_path
            ]
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            _, _ = await proc.communicate()
            return proc.returncode == 0
        except Exception:
            # If ffmpeg is not available (e.g. on basic serverless), fallback gracefully to mp3
            return False

    @classmethod
    async def generate_speech(
        cls, 
        text: str, 
        voice: str = "en-US-ChristopherNeural", 
        rate: str = "+0%", 
        pitch: str = "+0Hz",
        as_voice_note: bool = True
    ) -> str:
        # Use /tmp on Vercel as root filesystem is read-only
        temp_dir = "/tmp" if os.getenv("VERCEL") else os.path.join(os.path.dirname(__file__), "..", "temp")
        os.makedirs(temp_dir, exist_ok=True)
        
        # If user has auto-detect enabled, resolve voice dynamically
        if voice == "auto":
            voice = cls.detect_auto_voice(text)

        file_base = f"{abs(hash(text))}_{int(asyncio.get_event_loop().time() * 1000)}"
        mp3_path = os.path.join(temp_dir, f"{file_base}.mp3")
        ogg_path = os.path.join(temp_dir, f"{file_base}.ogg")

        if config.CUSTOM_TTS_API_URL:
            success = await cls._generate_via_custom_api(text, voice, mp3_path)
            if not success:
                await cls._generate_via_edge_tts(text, voice, rate, pitch, mp3_path)
        else:
            await cls._generate_via_edge_tts(text, voice, rate, pitch, mp3_path)

        if as_voice_note:
            converted = await cls.convert_mp3_to_ogg(mp3_path, ogg_path)
            if converted and os.path.exists(ogg_path):
                if os.path.exists(mp3_path):
                    os.remove(mp3_path)
                return ogg_path

        return mp3_path

    @staticmethod
    async def _generate_via_edge_tts(text: str, voice: str, rate: str, pitch: str, output_path: str):
        communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate, pitch=pitch)
        await communicate.save(output_path)

    @staticmethod
    async def _generate_via_custom_api(text: str, voice: str, output_path: str) -> bool:
        try:
            headers = {"Authorization": f"Bearer {config.CUSTOM_TTS_API_KEY}"} if config.CUSTOM_TTS_API_KEY else {}
            payload = {"input": text, "voice": voice, "model": "tts-1"}
            async with aiohttp.ClientSession() as session:
                async with session.post(config.CUSTOM_TTS_API_URL, json=payload, headers=headers, timeout=30) as resp:
                    if resp.status == 200:
                        content = await resp.read()
                        with open(output_path, "wb") as f:
                            f.write(content)
                        return True
        except Exception as e:
            print(f"Custom API failed, fallback to edge-tts: {e}")
        return False

tts_service = TTSService()
