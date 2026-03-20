/**
 * Trigger the vote-update GitHub Actions workflow via workflow_dispatch.
 */
export async function triggerVoteUpdate(): Promise<void> {
  const owner = process.env.GITHUB_REPO_OWNER;
  const name = process.env.GITHUB_REPO_NAME;
  const token = process.env.GITHUB_PAT;
  if (!owner || !name || !token) throw new Error("Missing GitHub env vars");

  const url = `https://api.github.com/repos/${owner}/${name}/actions/workflows/vote-update.yml/dispatches`;
  const res = await fetch(url, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      Accept: "application/vnd.github+json",
      "X-GitHub-Api-Version": "2022-11-28",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ ref: "main" }),
  });

  if (!res.ok && res.status !== 204) {
    throw new Error(`workflow_dispatch failed: ${res.status} ${await res.text()}`);
  }
}
