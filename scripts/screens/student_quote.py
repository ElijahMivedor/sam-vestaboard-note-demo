"""Student quote screen — cycles through config/quotes.json.

Layout (3 rows × 15 cols):
  Row 0: "** QUOTE **"  (centered)
  Row 1: first 15 chars of quote (word-wrapped)
  Row 2: second line or "- Author"
"""
import json
import os
from scripts.vbml_helper import center_string, fill_board, word_wrap

CONFIG_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "config", "quotes.json"
)


def render(state: dict) -> list[list[int]]:
    with open(CONFIG_PATH) as f:
        config = json.load(f)

    quotes = config["quotes"]
    if not quotes:
        return fill_board([center_string("NO QUOTES")])

    idx = state.get("rotation", {}).get("quote_sub_index", 0) % len(quotes)
    quote = quotes[idx]

    text = quote.get("text", "")
    author = quote.get("author", "")

    lines = word_wrap(text, width=15)

    row1 = lines[0] if len(lines) > 0 else ""
    # Row 2: continuation of quote or author attribution
    if len(lines) > 1:
        row2 = lines[1]
    else:
        row2 = f"-{author}"[:15]

    rows = [
        center_string("** QUOTE **"),
        center_string(row1),
        center_string(row2),
    ]
    return fill_board(rows)
