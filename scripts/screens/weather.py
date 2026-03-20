"""Weather screen — fetches current conditions from Open-Meteo (free, no key).

Layout (3 rows × 15 cols):
  Row 0: " *** WEATHER ***"  (centered, 15)
  Row 1: "NOW 72F  CLEAR "
  Row 2: "HI: 78F  LO:61F"
"""
import os
import requests
from scripts.vbml_helper import center_string, fill_board

WMO_CONDITIONS: dict[int, str] = {
    0: "CLEAR",
    1: "CLEAR", 2: "PT CLOUDY", 3: "CLOUDY",
    45: "FOG", 48: "FOG",
    51: "DRIZZLE", 53: "DRIZZLE", 55: "DRIZZLE",
    61: "RAIN", 63: "RAIN", 65: "HVY RAIN",
    71: "SNOW", 73: "SNOW", 75: "HVY SNOW",
    80: "SHOWERS", 81: "SHOWERS", 82: "SHOWERS",
    95: "TSTORM", 96: "TSTORM", 99: "TSTORM",
}


def _c_to_f(c: float) -> int:
    return round(c * 9 / 5 + 32)


def render(state: dict) -> list[list[int]]:
    lat = os.environ.get("OPENMETEO_LAT", "37.7749")
    lon = os.environ.get("OPENMETEO_LON", "-122.4194")
    tz = os.environ.get("OPENMETEO_TZ", "America/Los_Angeles")

    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,weathercode"
        f"&daily=temperature_2m_max,temperature_2m_min"
        f"&temperature_unit=celsius"
        f"&timezone={tz}"
        f"&forecast_days=1"
    )
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    current_c = data["current"]["temperature_2m"]
    wmo = data["current"]["weathercode"]
    hi_c = data["daily"]["temperature_2m_max"][0]
    lo_c = data["daily"]["temperature_2m_min"][0]

    now_f = _c_to_f(current_c)
    hi_f = _c_to_f(hi_c)
    lo_f = _c_to_f(lo_c)
    condition = WMO_CONDITIONS.get(wmo, "?")[:9]

    # 15 chars each
    row1 = f"NOW:{now_f}F {condition}"
    row2 = f"HI:{hi_f}F LO:{lo_f}F"

    rows = [
        center_string("* WEATHER *"),
        center_string(row1),
        center_string(row2),
    ]
    return fill_board(rows)
