# 🤝 Project Handoff: Voxify AI Voice Bot

This document contains everything needed to resume, maintain, and scale the **Voxify AI Voice Bot** in future sessions.

---

## 📌 Executive Summary & Key Credentials

| Property | Details |
| :--- | :--- |
| **Bot Name** | `Voxify — Озвучка текста \| ИИ Голос` |
| **Bot Username** | **`@VoxifyVoiceBot`** |
| **Bot ID** | `8910134664` |
| **Owner / Admin Telegram ID** | `5831301324` |
| **GitHub Repository** | [github.com/khamidkhl2/voxify-ai-voice-bot](https://github.com/khamidkhl2/voxify-ai-voice-bot) |
| **Live Webhook URL** | `https://voxify-ai-voice-bot.vercel.app/` |
| **Local Project Path** | `/Users/khamid/Documents/ai-tts-monetized-bot` |
| **Deployment Platform** | Vercel (Serverless Python Webhook) |

---

## 🚀 Current System Status

* **Status:** ✅ **LIVE & FULLY OPERATIONAL**
* **Deployment Workflow:** Connected to GitHub `main` branch. Any `git push` automatically redeploys on Vercel within ~30 seconds.
* **Telegram Webhook:** Configured and active. Updates are delivered instantly to the Vercel serverless function at `/`.

---

## 📁 Repository Structure

```text
ai-tts-monetized-bot/
├── api/
│   └── index.py            # Vercel Serverless Function entry point (handles webhooks & /set_webhook)
├── assets/
│   ├── avatar.jpg          # Clean 1:1 minimalist soundwave profile picture
│   └── welcome_banner.jpg  # 16:9 3D AI neural voice welcome banner
├── database/
│   ├── db.py               # Async SQLite manager (users, sponsors, referral counter, invoices)
│   └── bot_data.db         # Persistent local database (routed to /tmp on Vercel)
├── handlers/
│   ├── admin.py            # Admin panel: /admin, /add_sponsor, /sponsors, /broadcast, /give_vip
│   ├── advertise.py        # Automated ad order flow: /advertise, /sponsor, CryptoBot invoicing
│   ├── inline_mode.py      # Inline mode for group chat virality (@VoxifyVoiceBot <text>)
│   ├── sponsor_gate.py     # Callback handler for sponsor verification & VIP purchases
│   ├── start.py            # /start, /help, /referral, /lang, and Stars payment handler
│   ├── tts_handler.py      # Main text-to-speech request pipeline, gating check & ad footer
│   └── voice_settings.py   # Voice & dialect selection menu (/voice) & audio format toggles
├── keyboards/
│   └── inline.py           # Reusable inline keyboard layouts (i18n aware)
├── services/
│   ├── crypto_pay.py       # CryptoPay API client (@CryptoBot) for automated USDT/TON checkout
│   ├── i18n.py             # Multi-language dictionary (English, Russian, Spanish, Uzbek)
│   ├── sponsor_service.py  # getChatMember verification & quota delivery tracking engine
│   └── tts.py              # Neural speech synthesis (Edge-TTS) + auto language detector + ffmpeg
├── .env                    # Secret environment variables (ignored by Git)
├── .env.example            # Environment template for reference
├── .gitignore              # Protects secrets, DB, and temporary files from being committed
├── config.py               # Central configuration with safe fallback parsing
├── Dockerfile              # Container definition with Python 3.11 & FFmpeg (for Docker/VPS/Koyeb)
├── docker-compose.yml      # Local / VPS container runner
├── main.py                 # Long-polling runner (used for local testing or Docker deployments)
├── requirements.txt        # Python dependency manifest
├── MONETIZATION_PLAN.md    # Detailed blueprint for organic traffic and ad monetization
├── HANDOFF.md              # This transition document
└── vercel.json             # Vercel routing configuration
```

---

## ⚡️ Key Modules & Monetization Features

1. **Mandatory Subscription Gating (ОП / Ad-Gating):**
   * Located in `services/sponsor_service.py` & `handlers/sponsor_gate.py`.
   * Checks active sponsors from DB. Locks audio generation until verified with `getChatMember`.
   * Increments `delivered_subs` and auto-deactivates the channel once target quota is reached.
2. **Automated CryptoPay Checkout:**
   * Located in `services/crypto_pay.py` & `handlers/advertise.py`.
   * Channel owners run `/advertise`, select a tier (e.g. 500 subs for $15), and pay in USDT/TON via `@CryptoBot`.
3. **Telegram Stars VIP Subscription:**
   * Handled in `handlers/start.py` (`/vip`). Users pay 50 Stars for 30 days of ad-free access.
4. **Smart Auto-Detect Speech Engine:**
   * Located in `services/tts.py`. Automatically detects if text is Russian, Uzbek, English, Spanish, or Arabic and selects the best neural voice dynamically.
5. **Admin Control:**
   * Type `/admin` inside `@VoxifyVoiceBot` from account `5831301324` to view user counts, active sponsors, delivered subscribers, or send `/broadcast`.

---

## 📋 Next Session Action Plan

When resuming in the next session:
1. **First Sponsor Channel Activation:** Add your first sponsor channel or partner channel via `/add_sponsor` to test the live subscription-gating flow.
2. **CryptoPay Integration:** (Optional) If you want automated ad sales, get a token from [@CryptoBot](https://t.me/CryptoBot) (`/pay` -> Create App) and paste it into Vercel's Environment Variables (`CRYPTO_PAY_TOKEN`).
3. **Traffic Launch:** Execute the short-form viral funnel (TikTok/Reels/Shorts clips featuring the AI voices) to bring the first wave of 1,000+ active users into the bot.
