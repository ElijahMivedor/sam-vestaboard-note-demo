/**
 * GitHub Contents API helpers with SHA-based optimistic concurrency.
 * Used by the Vercel API routes to read/write state/votes.json.
 */

const GITHUB_API = "https://api.github.com";

function headers(): HeadersInit {
  const token = process.env.GITHUB_PAT;
  if (!token) throw new Error("GITHUB_PAT env var is not set");
  return {
    Authorization: `Bearer ${token}`,
    Accept: "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
    "Content-Type": "application/json",
  };
}

function repo(): string {
  const owner = process.env.GITHUB_REPO_OWNER;
  const name = process.env.GITHUB_REPO_NAME;
  if (!owner || !name) throw new Error("GITHUB_REPO_OWNER / GITHUB_REPO_NAME not set");
  return `${owner}/${name}`;
}

export interface VotesData {
  question: string;
  option_a: string;
  option_b: string;
  votes_a: number;
  votes_b: number;
}

export async function readVotes(): Promise<{ data: VotesData; sha: string }> {
  const url = `${GITHUB_API}/repos/${repo()}/contents/state/votes.json`;
  const res = await fetch(url, { headers: headers(), cache: "no-store" });
  if (!res.ok) throw new Error(`GitHub API error: ${res.status} ${await res.text()}`);

  const body = await res.json();
  const content = Buffer.from(body.content, "base64").toString("utf-8");
  return { data: JSON.parse(content), sha: body.sha };
}

export async function writeVotes(
  data: VotesData,
  sha: string,
  message: string
): Promise<string> {
  const url = `${GITHUB_API}/repos/${repo()}/contents/state/votes.json`;
  const contentB64 = Buffer.from(JSON.stringify(data, null, 2)).toString("base64");

  for (let attempt = 0; attempt < 2; attempt++) {
    const res = await fetch(url, {
      method: "PUT",
      headers: headers(),
      body: JSON.stringify({ message, content: contentB64, sha }),
    });

    if (res.status === 409 && attempt === 0) {
      // Conflict — re-read SHA and retry
      const fresh = await readVotes();
      sha = fresh.sha;
      continue;
    }
    if (!res.ok) throw new Error(`GitHub write error: ${res.status} ${await res.text()}`);
    const body = await res.json();
    return body.content.sha;
  }

  throw new Error("Failed to write votes after retry");
}
