"""Screen registry: maps screen name → render function.

Each render function signature:
    render(state: dict) -> list[list[int]]

Where `state` is a dict with keys:
    rotation  – contents of state/rotation.json
    votes     – contents of state/votes.json
"""
from scripts.screens.weather import render as render_weather
from scripts.screens.office_hours import render as render_office_hours
from scripts.screens.news import render as render_news
from scripts.screens.this_or_that import render as render_this_or_that
from scripts.screens.student_quote import render as render_student_quote

REGISTRY: dict[str, callable] = {
    "weather": render_weather,
    "office_hours": render_office_hours,
    "news": render_news,
    "this_or_that": render_this_or_that,
    "student_quote": render_student_quote,
}
