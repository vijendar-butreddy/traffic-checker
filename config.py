import os
from dotenv import load_dotenv

load_dotenv()

def get_config():
    config = {
        # Google Maps
        "GOOGLE_MAPS_API_KEY": os.getenv("GOOGLE_MAPS_API_KEY"),

        # Telegram
        "TELEGRAM_BOT_TOKEN": os.getenv("TELEGRAM_BOT_TOKEN"),
        "TELEGRAM_CHAT_ID": os.getenv("TELEGRAM_CHAT_ID"),

        # Route
        "ORIGIN": os.getenv("ORIGIN"),
        "DESTINATION": os.getenv("DESTINATION"),

        # Schedule
        "MORNING_CHECK_TIME": os.getenv("MORNING_CHECK_TIME", "08:00"),
        "EVENING_CHECK_TIME": os.getenv("EVENING_CHECK_TIME", "15:30"),
        "TIMEZONE": os.getenv("TIMEZONE", "America/Chicago"),

        # Alert threshold — 1.3 means alert if trip is 30% longer than usual
        "TRAFFIC_THRESHOLD": float(os.getenv("TRAFFIC_THRESHOLD", "1.3")),
    }

    # Validate required fields
    required = [
        "GOOGLE_MAPS_API_KEY",
        "TELEGRAM_BOT_TOKEN",
        "TELEGRAM_CHAT_ID",
        "ORIGIN",
        "DESTINATION",
    ]
    missing = [key for key in required if not config[key]]
    if missing:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")

    return config
