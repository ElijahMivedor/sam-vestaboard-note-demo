"""News screen — fetches top headline from an RSS feed.

Layout (3 rows × 15 cols):
  Row 0: "*** NEWS ***"  (centered)
  Rows 1-2: word-wrapped headline (2 lines × 15 chars)
"""
import os
import feedparser
from scripts.vbml_helper import center_string, fill_board, word_wrap


def render(state: dict) -> list[list[int]]:
    rss_url = os.environ.get(
        "NEWS_RSS_URL", "https://feeds.npr.org/1001/rss.xml"
    )
    feed = feedparser.parse(rss_url)

    headline = "NO NEWS TODAY"
    if feed.entries:
        headline = feed.entries[0].get("title", headline)
        # Strip trailing source attribution like " : NPR"
        if " : " in headline:
            headline = headline.split(" : ")[0]

    lines = word_wrap(headline, width=15)[:2]

    rows: list[list[int]] = [center_string("*** NEWS ***")]
    for line in lines:
        rows.append(center_string(line))

    return fill_board(rows)
