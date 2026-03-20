"""Rotation entrypoint.

Usage:
    python scripts/rotate.py [--force-screen SCREEN_NAME]

Steps:
1. Small random sleep to avoid collisions with simultaneous runs.
2. Read state/rotation.json (with SHA).
3. Advance current_index (or use --force-screen).
4. Write updated rotation.json back to repo.
5. Read state/votes.json.
6. Look up screen renderer from REGISTRY.
7. Call renderer → get 6×22 character array.
8. POST to Vestaboard.
"""
import argparse
import json
import os
import random
import sys
import time
from datetime import datetime, timezone

# Ensure repo root is on path when run from Actions working directory
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.update_state import read_json, write_json
from scripts.post_to_vestaboard import post_to_vestaboard
from scripts.screens import REGISTRY


def load_screens_config() -> list[str]:
    config_path = os.path.join(
        os.path.dirname(__file__), "..", "config", "screens.json"
    )
    with open(config_path) as f:
        return json.load(f)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force-screen", default=None)
    args = parser.parse_args()

    # Jitter to avoid simultaneous-run collisions
    jitter = random.uniform(0, 5)
    print(f"[rotate] Sleeping {jitter:.1f}s jitter…")
    time.sleep(jitter)

    # --- Read rotation state ---
    rotation, rotation_sha = read_json("state/rotation.json")
    votes, _ = read_json("state/votes.json")

    screens = load_screens_config()
    n = len(screens)

    if args.force_screen:
        screen_name = args.force_screen
        new_index = rotation["current_index"]  # Don't advance on force
        print(f"[rotate] Forced screen: {screen_name}")
    else:
        new_index = (rotation["current_index"] + 1) % n
        screen_name = screens[new_index]
        print(f"[rotate] Advancing to index {new_index}: {screen_name}")

    # Advance quote sub-index if showing student_quote
    new_quote_idx = rotation.get("quote_sub_index", 0)
    if screen_name == "student_quote":
        new_quote_idx = (new_quote_idx + 1) % 100  # will be clamped in renderer

    # --- Write updated rotation state (before rendering, so crashes don't loop) ---
    if not args.force_screen:
        updated_rotation = {
            "current_index": new_index,
            "quote_sub_index": new_quote_idx,
            "last_updated": datetime.now(timezone.utc).isoformat(),
        }
        write_json(
            "state/rotation.json",
            updated_rotation,
            rotation_sha,
            f"chore: advance rotation to {screen_name}",
        )
        print(f"[rotate] State updated.")

    # --- Render screen ---
    if screen_name not in REGISTRY:
        print(f"[rotate] ERROR: unknown screen '{screen_name}'. Known: {list(REGISTRY)}")
        sys.exit(1)

    state = {
        "rotation": {**rotation, "current_index": new_index, "quote_sub_index": new_quote_idx},
        "votes": votes,
    }

    print(f"[rotate] Rendering {screen_name}…")
    characters = REGISTRY[screen_name](state)

    # --- Post to Vestaboard ---
    post_to_vestaboard(characters)
    print(f"[rotate] Done.")


if __name__ == "__main__":
    main()
