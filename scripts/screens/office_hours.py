"""Office hours screen — reads config/office_hours.json.

Layout (3 rows × 15 cols):
  Row 0: "* OFF. HOURS *"  (centered)
  Row 1: "MON 2-4PM R101"
  Row 2: "WED 1-3PM R204"
"""
import json
import os
from scripts.vbml_helper import center_string, fill_board

CONFIG_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "config", "office_hours.json"
)


def render(state: dict) -> list[list[int]]:
    with open(CONFIG_PATH) as f:
        config = json.load(f)

    rows: list[list[int]] = [
        center_string("*OFF HOURS*"),
    ]

    for entry in config["schedule"][:2]:
        day = entry["day"][:3].upper()
        time_str = entry["time"][:6].upper()
        # Shorten room: "RM 101" -> "R101"
        room = entry["room"].replace("RM ", "R").replace(" ", "")[:4].upper()
        line = f"{day} {time_str} {room}"
        rows.append(center_string(line))

    return fill_board(rows)
