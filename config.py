import os
from dataclasses import dataclass
from typing import List
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    ADMIN_IDS: List[int] = None
    
    # Monetization Settings
    # CryptoPay API token from @CryptoBot (https://t.me/CryptoBot -> /pay)
    CRYPTO_PAY_TOKEN: str = os.getenv("CRYPTO_PAY_TOKEN", "")
    CRYPTO_PAY_NET: str = os.getenv("CRYPTO_PAY_NET", "mainnet") # mainnet or testnet
    
    # Pricing for advertisers: Price in USD for sponsor packages
    SPONSOR_TIERS = {
        "tier_500": {"subs": 500, "price_usd": 15.0},
        "tier_1000": {"subs": 1000, "price_usd": 25.0},
        "tier_2500": {"subs": 2500, "price_usd": 50.0},
    }
    
    # VIP user pricing in Telegram Stars (if they want to bypass mandatory subs)
    VIP_PRICE_STARS: int = int(os.getenv("VIP_PRICE_STARS", "50")) # 50 Telegram Stars (~$1)
    
    # Free referrals needed to get 1 month of VIP ad-free
    REFERRALS_FOR_VIP: int = int(os.getenv("REFERRALS_FOR_VIP", "3"))
    
    # Custom TTS API settings (optional, defaults to edge-tts if empty)
    CUSTOM_TTS_API_URL: str = os.getenv("CUSTOM_TTS_API_URL", "")
    CUSTOM_TTS_API_KEY: str = os.getenv("CUSTOM_TTS_API_KEY", "")
    
    # Fallback ad link if no paid sponsor is currently active
    FALLBACK_AD_TEXT: str = os.getenv("FALLBACK_AD_TEXT", "📢 Advertise your channel here! Tap /advertise")
    FALLBACK_AD_URL: str = os.getenv("FALLBACK_AD_URL", "https://t.me/CryptoBot")

    def __post_init__(self):
        admin_str = os.getenv("ADMIN_IDS", "")
        self.ADMIN_IDS = [int(x.strip()) for x in admin_str.split(",") if x.strip().isdigit()]

config = Config()
