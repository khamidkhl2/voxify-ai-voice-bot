# 🎙 AI Text-to-Speech (TTS) Monetized Telegram Bot

A complete, production-ready Telegram Bot for AI Text-to-Speech generation with **built-in automated monetization** and viral growth loops.

---

## 💰 Monetization Engines Included

1. **Mandatory Subscription Gating (ОП / Ad-Gating):**
   * Forces users to join sponsor channels before they can generate audio.
   * Automatically verifies subscriptions using Telegram's `getChatMember`.
   * Automatically counts delivered subscribers and deactivates channels once target is met.
2. **Automated Advertiser Checkout (@CryptoBot / CryptoPay):**
   * Channel owners run `/advertise` to choose a package (e.g. 500 subs for $15, 1,000 for $25).
   * Generates instant CryptoBot invoices (USDT, TON, BTC).
   * Automatically activates the channel upon payment detection.
3. **Telegram Stars VIP Pass:**
   * Power users can buy an Ad-Free VIP Pass using native Telegram Stars (`/vip`).
4. **Viral Forward Loop & Audio Watermarking:**
   * Every generated audio note includes an inline button: `"🗣 Voice your own text with @YourBot"`.
   * When users forward voice messages to friends or groups, new users flow into your bot.
5. **Inline Mode (`@YourBot ...`):**
   * Users can generate voice messages directly inside group chats, exposing your bot to hundreds of group members for free.

---

## 🚀 Quick Setup Guide

### 1. Configure Environment
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Edit `.env` and fill in:
* `BOT_TOKEN`: Your bot token from [@BotFather](https://t.me/BotFather).
* `ADMIN_IDS`: Your Telegram ID (get it from [@userinfobot](https://t.me/userinfobot)).
* `CRYPTO_PAY_TOKEN`: (Optional) Get an API token from [@CryptoBot](https://t.me/CryptoBot) by typing `/pay` -> `Create App`.
* `CUSTOM_TTS_API_URL`: (Optional) If you have a custom free TTS API, enter its URL. Otherwise, the bot uses free high-definition Microsoft Neural voices (`edge-tts`).

### 2. Enable Inline Mode in BotFather (Critical for Virality)
1. Open [@BotFather](https://t.me/BotFather).
2. Send `/setinline`.
3. Choose your bot and send a placeholder query (e.g., `Type text to generate speech...`).

### 3. Run the Bot
```bash
./venv/bin/python3 main.py
```

---

## 👑 Admin Commands

* `/admin` - View total users, VIP members, active sponsors, and delivered subscribers.
* `/add_sponsor <channel_id> <invite_link> <target_subs> <Title>` - Manually add a sponsor channel.
  * *Example:* `/add_sponsor @tech_daily https://t.me/tech_daily 500 Tech Daily News`
  * *Important:* Add your bot as an **Administrator** in the sponsor channel so it can check member statuses.
* `/sponsors` - View and delete active sponsor channels.
* `/broadcast <HTML text>` - Send a sponsored message or announcement to every user in the database.
* `/give_vip <user_id> [days]` - Grant VIP status manually to any user.

---

## 🛠 Custom TTS API Integration

By default, the bot uses `edge-tts` (zero cost, 300+ ultra-realistic voices across 50+ languages).

If you want to plug in your own free API or proxy endpoint, set in `.env`:
```env
CUSTOM_TTS_API_URL=https://your-custom-api.com/v1/audio/speech
CUSTOM_TTS_API_KEY=your_key_here
```
The adapter inside `services/tts.py` handles the requests automatically.
