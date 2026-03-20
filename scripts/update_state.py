"""Read and write JSON state files in the GitHub repo via the Contents API.

Uses SHA-based optimistic concurrency: fetch the current SHA, then PUT with
that SHA. On 409 Conflict, retry once after re-reading the SHA.
"""
import base64
import json
import os
import time
import requests

GITHUB_API = "https://api.github.com"


def _headers() -> dict[str, str]:
    token = os.environ["GITHUB_TOKEN"]
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def _repo() -> str:
    owner = os.environ["GITHUB_REPOSITORY_OWNER"]
    repo_full = os.environ["GITHUB_REPOSITORY"]  # owner/repo
    repo = repo_full.split("/")[-1]
    return f"{owner}/{repo}"


def read_json(path: str) -> tuple[dict, str]:
    """Read a JSON file from the repo. Returns (data, sha)."""
    url = f"{GITHUB_API}/repos/{_repo()}/contents/{path}"
    resp = requests.get(url, headers=_headers(), timeout=10)
    resp.raise_for_status()
    body = resp.json()
    content = base64.b64decode(body["content"]).decode()
    return json.loads(content), body["sha"]


def write_json(path: str, data: dict, sha: str, message: str) -> str:
    """Write a JSON file to the repo. Returns new SHA. Retries once on 409."""
    url = f"{GITHUB_API}/repos/{_repo()}/contents/{path}"
    content_b64 = base64.b64encode(
        json.dumps(data, indent=2).encode()
    ).decode()

    for attempt in range(2):
        payload = {
            "message": message,
            "content": content_b64,
            "sha": sha,
        }
        resp = requests.put(url, headers=_headers(), json=payload, timeout=10)
        if resp.status_code == 409 and attempt == 0:
            # Conflict — re-read SHA and retry
            print(f"[update_state] 409 conflict on {path}, re-reading SHA…")
            time.sleep(1)
            _, sha = read_json(path)
            continue
        resp.raise_for_status()
        return resp.json()["content"]["sha"]

    raise RuntimeError(f"Failed to write {path} after retry")
