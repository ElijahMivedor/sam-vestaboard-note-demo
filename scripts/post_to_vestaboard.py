"""Post a 6x22 character code array to the Vestaboard Read-Write API."""
import os
import requests

VESTABOARD_API_URL = "https://rw.vestaboard.com/"


def post_to_vestaboard(characters: list[list[int]]) -> None:
    """Post a 6x22 character code grid to Vestaboard.

    Args:
        characters: 6 rows × 22 columns of Vestaboard character codes.

    Raises:
        ValueError: If the grid dimensions are wrong.
        requests.HTTPError: If the API call fails.
    """
    if len(characters) != 3:
        raise ValueError(f"Expected 3 rows, got {len(characters)}")
    for i, row in enumerate(characters):
        if len(row) != 15:
            raise ValueError(f"Row {i} has {len(row)} columns, expected 15")

    token = os.environ["VESTABOARD_TOKEN"]
    response = requests.post(
        VESTABOARD_API_URL,
        headers={
            "X-Vestaboard-Read-Write-Key": token,
            "Content-Type": "application/json",
        },
        json=characters,
        timeout=15,
    )
    response.raise_for_status()
    print(f"[vestaboard] Posted successfully: HTTP {response.status_code}")
