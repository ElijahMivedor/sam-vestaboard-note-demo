"""This or That voting screen — reads state/votes.json.

Layout (3 rows × 15 cols):
  Row 0: "THIS OR THAT"  (centered)
  Row 1: "A:<opt>  XX%"  truncated to 15
  Row 2: "B:<opt>  YY%"  truncated to 15
"""
from scripts.vbml_helper import center_string, fill_board, encode_string


def render(state: dict) -> list[list[int]]:
    votes = state.get("votes", {})
    option_a = votes.get("option_a", "Option A")
    option_b = votes.get("option_b", "Option B")
    votes_a = votes.get("votes_a", 0)
    votes_b = votes.get("votes_b", 0)

    total = votes_a + votes_b
    pct_a = round(votes_a / total * 100) if total else 0
    pct_b = round(votes_b / total * 100) if total else 0

    # Truncate option names to leave room for "A:  XX%" (7 chars) → 8 chars for name
    a_label = option_a[:8].upper()
    b_label = option_b[:8].upper()

    a_line = f"A:{a_label} {pct_a}%"[:15]
    b_line = f"B:{b_label} {pct_b}%"[:15]

    rows = [
        center_string("THISOR THAT"),
        encode_string(a_line),
        encode_string(b_line),
    ]
    return fill_board(rows)
