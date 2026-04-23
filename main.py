import logging
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz

from config import get_config
from checker import check_traffic
from notifier import send_telegram_message, build_alert_message

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)


def run_check(direction: str):
    """
    Runs a traffic check and sends a Telegram alert if congested.
    direction: "morning" or "evening"
    """
    log.info(f"Running {direction} traffic check...")

    try:
        config = get_config()
    except EnvironmentError as e:
        log.error(f"Config error: {e}")
        return

    # For evening commute, swap origin and destination
    origin = config["ORIGIN"] if direction == "morning" else config["DESTINATION"]
    destination = config["DESTINATION"] if direction == "morning" else config["ORIGIN"]

    result = check_traffic(
        origin=origin,
        destination=destination,
        api_key=config["GOOGLE_MAPS_API_KEY"],
        threshold=config["TRAFFIC_THRESHOLD"],
    )

    if not result["ok"]:
        log.error(f"Traffic check failed: {result['error']}")
        # Optionally notify about the error too
        send_telegram_message(
            config["TELEGRAM_BOT_TOKEN"],
            config["TELEGRAM_CHAT_ID"],
            f"⚠️ Traffic checker error: {result['error']}"
        )
        return

    log.info(
        f"Result — Normal: {result['normal_mins']}m, "
        f"With traffic: {result['traffic_mins']}m, "
        f"Ratio: {result['ratio']:.2f}, "
        f"Congested: {result['is_congested']}"
    )

    if result["is_congested"]:
        message = build_alert_message(result, direction=direction)
        success = send_telegram_message(
            config["TELEGRAM_BOT_TOKEN"],
            config["TELEGRAM_CHAT_ID"],
            message,
        )
        if success:
            log.info("Alert sent via Telegram.")
        else:
            log.error("Failed to send Telegram alert.")
    else:
        log.info("No significant traffic. No notification sent. ✅")


def morning_check():
    run_check("morning")


def evening_check():
    run_check("evening")


def main():
    config = get_config()
    tz = pytz.timezone(config["TIMEZONE"])

    morning_hour, morning_minute = map(int, config["MORNING_CHECK_TIME"].split(":"))
    evening_hour, evening_minute = map(int, config["EVENING_CHECK_TIME"].split(":"))

    scheduler = BlockingScheduler(timezone=tz)

    scheduler.add_job(
        morning_check,
        trigger=CronTrigger(hour=morning_hour, minute=morning_minute, timezone=tz),
        id="morning_check",
        name="Morning traffic check",
    )

    scheduler.add_job(
        evening_check,
        trigger=CronTrigger(hour=evening_hour, minute=evening_minute, timezone=tz),
        id="evening_check",
        name="Evening traffic check",
    )

    log.info(f"Scheduler started. Timezone: {config['TIMEZONE']}")
    log.info(f"Morning check at {config['MORNING_CHECK_TIME']}")
    log.info(f"Evening check at {config['EVENING_CHECK_TIME']}")
    log.info(f"Route: {config['ORIGIN']}  →  {config['DESTINATION']}")
    log.info(f"Alert threshold: {config['TRAFFIC_THRESHOLD']}x normal duration")

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        log.info("Scheduler stopped.")


if __name__ == "__main__":
    main()
