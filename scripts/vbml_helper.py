"""Helpers for building Vestaboard character code arrays.

Vestaboard character codes (subset used here):
  0  = blank
  1-26  = A-Z
  27 = ! 28 = @ 29 = # 30 = $ 31 = %
  37 = & 44 = - 46 = . 47 = /
  52-61 = 0-9
  62 = : 63 = ; 65 = ? 67 = "
  68-73 = red/orange/yellow/green/blue/violet (filled squares)

ROWS = 6, COLS = 22
"""

ROWS = 3
COLS = 15

# Character code lookup
_CHAR_MAP: dict[str, int] = {
    " ": 0,
    "!": 27,
    "@": 28,
    "#": 29,
    "$": 30,
    "%": 31,
    "&": 37,
    "-": 44,
    ".": 46,
    "/": 47,
    ":": 62,
    ";": 63,
    "?": 65,
    '"': 67,
    "'": 52,  # closest available
}

# A-Z → 1-26
for _i, _c in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    _CHAR_MAP[_c] = _i + 1

# 0-9 → 52-61
for _i, _c in enumerate("0123456789"):
    _CHAR_MAP[_c] = _i + 52


def char_code(ch: str) -> int:
    """Return the Vestaboard character code for a single character."""
    return _CHAR_MAP.get(ch.upper(), 0)


def encode_string(text: str, width: int = COLS) -> list[int]:
    """Encode a string into a list of character codes, padded/truncated to `width`."""
    codes = [char_code(c) for c in text.upper()]
    if len(codes) < width:
        codes += [0] * (width - len(codes))
    return codes[:width]


def center_string(text: str, width: int = COLS) -> list[int]:
    """Center text within `width` columns."""
    text = text.upper()
    total_pad = width - len(text)
    left = total_pad // 2
    padded = " " * left + text
    return encode_string(padded, width)


def blank_row() -> list[int]:
    """Return an empty row (all zeros)."""
    return [0] * COLS


def blank_board() -> list[list[int]]:
    """Return a blank 6×22 board."""
    return [blank_row() for _ in range(ROWS)]


def word_wrap(text: str, width: int = COLS) -> list[str]:
    """Wrap text into lines of at most `width` characters."""
    words = text.upper().split()
    lines: list[str] = []
    current = ""
    for word in words:
        if len(word) > width:
            # Force-break long words
            while len(word) > width:
                lines.append(word[:width])
                word = word[width:]
            current = word
        elif current and len(current) + 1 + len(word) > width:
            lines.append(current)
            current = word
        else:
            current = (current + " " + word).strip()
    if current:
        lines.append(current)
    return lines


def fill_board(rows: list[list[int]]) -> list[list[int]]:
    """Pad a list of rows to 6 rows, each 22 columns."""
    result = [row[:COLS] + [0] * max(0, COLS - len(row)) for row in rows]
    while len(result) < ROWS:
        result.append(blank_row())
    return result[:ROWS]
