import requests
import json  # FONDAMENTALE: mancava questo
import os
from typing import Optional, Dict, List

class WeatherEngine:
    @staticmethod
    def fetch_data(city: str) -> Optional[Dict]:
        try:
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
            geo_res = requests.get(geo_url, timeout=5).json()
            if "results" not in geo_res: return None
            loc = geo_res["results"][0]

            w_url = (f"https://api.open-meteo.com/v1/forecast?latitude={loc['latitude']}"
                     f"&longitude={loc['longitude']}&current_weather=true"
                     f"&daily=temperature_2m_max,weathercode&timezone=auto&forecast_days=3")

            w_res = requests.get(w_url, timeout=5).json()

            forecasts = []
            for i in range(3):
                forecasts.append({
                    "date": w_res["daily"]["time"][i],
                    "temp_max": w_res["daily"]["temperature_2m_max"][i],
                    "code": w_res["daily"]["weathercode"][i]
                })

            return {
                "name": loc['name'],
                "current_temp": w_res["current_weather"]["temperature"],
                "current_code": w_res["current_weather"]["weathercode"],
                "forecasts": forecasts
            }
        except Exception as e:
            print(f"Errore nel fetch: {e}")
            return None

    @staticmethod
    def get_weather_icon(code: int) -> str:
        if code == 0: return "☀️"
        if 1 <= code <= 3: return "🌤️"
        if code >= 51: return "🌧️"
        return "☁️"

    @staticmethod
    def get_favorites() -> list:
        if not os.path.exists("favorites.json"):
            return []
        try:
            with open("favorites.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    @staticmethod
    def add_favorite(city: str) -> bool:
        favorites = WeatherEngine.get_favorites()
        city = city.strip().capitalize()
        if city and city not in favorites:
            favorites.append(city)
            with open("favorites.json", "w", encoding="utf-8") as f:
                json.dump(favorites, f, indent=4)
            return True
        return False

    @staticmethod
    def to_fahrenheit(celsius: float) -> float:
        return round((celsius * 9 / 5) + 32, 1)