import requests


def send_telegram_message(bot_token, chat_id, message):
    """
    Sends a message via Telegram Bot API.
    Returns True on success, False on failure.
    """
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"[Notifier] Failed to send Telegram message: {e}")
        return False


def build_alert_message(result, direction="morning"):
    """
    Builds a friendly Telegram alert message from the traffic check result.
    """
    arrow = "🌅" if direction == "morning" else "🌆"
    label = "morning commute" if direction == "morning" else "evening commute"

    lines = [
        f"{arrow} *Traffic Alert — {label.title()}*",
        f"",
        f"🚗 Route: _{result['summary']}_",
        f"⏱ Normal time: {result['normal_mins']} mins",
        f"🚦 Current time: {result['traffic_mins']} mins",
        f"⚠️ Extra delay: +{result['delay_mins']} mins ({int((result['ratio'] - 1) * 100)}% longer)",
        f"",
        f"📍 {result['origin_address']}",
        f"➡️ {result['destination_address']}",
        f"",
        f"_Consider leaving earlier or taking an alternate route._",
    ]

    return "\n".join(lines)
