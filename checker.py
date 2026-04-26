import requests
from datetime import datetime


def check_traffic(origin, destination, api_key, threshold):
    """
    Calls Google Maps Directions API and compares
    current travel time vs normal travel time.
    Returns a dict with status and details.
    """
    url = "https://maps.googleapis.com/maps/api/directions/json"

    params = {
        "origin": origin,
        "destination": destination,
        "departure_time": "now",
        "traffic_model": "best_guess",
        "key": api_key,
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data["status"] != "OK":
            return {
                "ok": False,
                "error": f"Maps API returned status: {data['status']}"
            }

        leg = data["routes"][0]["legs"][0]

        normal_duration_sec = leg["duration"]["value"]           # without traffic
        # duration_in_traffic may be absent if traffic data unavailable
        traffic_duration_sec = leg.get("duration_in_traffic", leg["duration"])["value"]

        normal_mins = normal_duration_sec // 60
        traffic_mins = traffic_duration_sec // 60
        delay_mins = traffic_mins - normal_mins
        ratio = traffic_duration_sec / normal_duration_sec

        is_congested = ratio >= threshold

        return {
            "ok": True,
            "is_congested": is_congested,
            "normal_mins": normal_mins,
            "traffic_mins": traffic_mins,
            "delay_mins": delay_mins,
            "ratio": ratio,
            "summary": data["routes"][0].get("summary", "your route"),
            "origin_address": leg.get("start_address", origin),
            "destination_address": leg.get("end_address", destination),
        }

    except requests.exceptions.RequestException as e:
        return {
            "ok": False,
            "error": f"Request failed: {str(e)}"
        }
    except (KeyError, IndexError) as e:
        return {
            "ok": False,
            "error": f"Unexpected API response format: {str(e)}"
        }
