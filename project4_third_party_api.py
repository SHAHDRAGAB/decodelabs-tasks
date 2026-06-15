"""
Project 4: Third-Party API Integration
Goal: Fetch and process data from an external server (e.g., Weather API).
Key Skills: Asynchronous programming, API key management, error handling.
"""

import os
import httpx
from flask import Flask, jsonify, request
from dotenv import load_dotenv

# Load API key securely from .env file
load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

app = Flask(__name__)


def fetch_weather(city: str) -> dict:
    """
    Fetches weather data from OpenWeatherMap API for the given city.
    Returns reformatted data for our users.
    """
    if not WEATHER_API_KEY:
        raise EnvironmentError("WEATHER_API_KEY is not set in .env file")

    params = {
        "q": city,
        "appid": WEATHER_API_KEY,
        "units": "metric",  # Celsius
    }

    # Synchronous HTTP request using httpx (easy to switch to async later)
    response = httpx.get(WEATHER_BASE_URL, params=params, timeout=10)

    if response.status_code == 404:
        raise ValueError(f"City '{city}' not found")

    if response.status_code == 401:
        raise PermissionError("Invalid API key")

    response.raise_for_status()
    raw = response.json()

    # Reformat and serve clean data to our users
    return {
        "city": raw["name"],
        "country": raw["sys"]["country"],
        "temperature_celsius": raw["main"]["temp"],
        "feels_like": raw["main"]["feels_like"],
        "humidity_percent": raw["main"]["humidity"],
        "condition": raw["weather"][0]["description"],
        "wind_speed_mps": raw["wind"]["speed"],
    }


# GET /weather?city=Cairo
@app.route("/weather", methods=["GET"])
def get_weather():
    city = request.args.get("city")

    if not city:
        return jsonify({"status": "error", "message": "Missing 'city' query parameter"}), 400

    try:
        weather_data = fetch_weather(city)
        return jsonify({"status": "ok", "data": weather_data}), 200

    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 404

    except PermissionError as e:
        return jsonify({"status": "error", "message": str(e)}), 401

    except EnvironmentError as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    except httpx.RequestError as e:
        return jsonify({"status": "error", "message": f"Network error: {str(e)}"}), 503

    except Exception as e:
        return jsonify({"status": "error", "message": f"Unexpected error: {str(e)}"}), 500


# Health check
@app.route("/", methods=["GET"])
def index():
    return jsonify({"status": "ok", "message": "Third-Party API Integration is running"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5001)
