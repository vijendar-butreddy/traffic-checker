# 🚦 Traffic Checker Bot

A lightweight Python app that checks your daily commute route for traffic congestion and sends you a **Telegram notification only when there's a problem**. No alert = smooth sailing. ✅

Runs on free cloud hosting (Railway) — no PC needs to be on.

---

## Features

- Checks traffic at configurable times (default: 8:00 AM and 3:30 PM)
- Automatically reverses route for evening commute
- Only notifies you if traffic exceeds your threshold (e.g. 30% longer than normal)
- Fully configurable via environment variables — works for any route, any timezone
- Free to run (Google Maps free tier + Railway free tier + Telegram free API)

---

## Setup

### 1. Get your API keys

**Google Maps:**
1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create a project, enable **Directions API**
3. Create an API key under Credentials

**Telegram Bot:**
1. Open Telegram → search **@BotFather** → `/newbot`
2. Save the **Bot Token** it gives you
3. Search **@userinfobot** → start it → save your **Chat ID**

### 2. Clone and configure

```bash
git clone https://github.com/YOUR_USERNAME/traffic-checker.git
cd traffic-checker
cp .env.example .env
# Edit .env with your values
```

### 3. Run locally

```bash
pip install -r requirements.txt
python main.py
```

### 4. Deploy to Railway

1. Push repo to GitHub
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Add all environment variables from your `.env` in Railway's dashboard
4. Done — it runs 24/7 for free!

---

## Configuration

| Variable | Description | Default |
|---|---|---|
| `GOOGLE_MAPS_API_KEY` | Your Maps API key | required |
| `TELEGRAM_BOT_TOKEN` | Your bot token from BotFather | required |
| `TELEGRAM_CHAT_ID` | Your Telegram chat ID | required |
| `ORIGIN` | Start address of your commute | required |
| `DESTINATION` | End address of your commute | required |
| `MORNING_CHECK_TIME` | Time for morning check (24h) | `08:00` |
| `EVENING_CHECK_TIME` | Time for evening check (24h) | `15:30` |
| `TIMEZONE` | Your local timezone | `America/Chicago` |
| `TRAFFIC_THRESHOLD` | Alert if trip is X times longer | `1.3` |

---

## Example Alert

```
🌅 Traffic Alert — Morning Commute

🚗 Route: via I-35
⏱ Normal time: 22 mins
🚦 Current time: 34 mins
⚠️ Extra delay: +12 mins (54% longer)

📍 123 Main St, Ankeny, IA
➡️ 456 Work Ave, Des Moines, IA

Consider leaving earlier or taking an alternate route.
```

---

## License

MIT — use it
