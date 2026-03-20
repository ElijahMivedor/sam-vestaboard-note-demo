"use client";

import { useEffect, useState } from "react";

interface VotesData {
  question: string;
  option_a: string;
  option_b: string;
  votes_a: number;
  votes_b: number;
}

export default function VotePage() {
  const [votes, setVotes] = useState<VotesData | null>(null);
  const [voted, setVoted] = useState<"a" | "b" | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("/api/votes")
      .then((r) => r.json())
      .then(setVotes)
      .catch(() => setError("Failed to load votes."));
  }, []);

  async function castVote(side: "a" | "b") {
    if (voted || loading) return;
    setLoading(true);
    try {
      const res = await fetch("/api/vote", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ side }),
      });
      if (!res.ok) throw new Error(await res.text());
      const updated = await res.json();
      setVotes(updated);
      setVoted(side);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Vote failed.");
    } finally {
      setLoading(false);
    }
  }

  if (error) {
    return <main style={styles.main}><p style={{ color: "#f66" }}>{error}</p></main>;
  }

  if (!votes) {
    return <main style={styles.main}><p>Loading…</p></main>;
  }

  const total = votes.votes_a + votes.votes_b;
  const pctA = total ? Math.round((votes.votes_a / total) * 100) : 0;
  const pctB = total ? Math.round((votes.votes_b / total) * 100) : 0;

  return (
    <main style={styles.main}>
      <h1 style={styles.title}>This or That?</h1>
      <p style={styles.question}>{votes.question}</p>

      <div style={styles.buttons}>
        <button
          style={{ ...styles.btn, ...(voted === "a" ? styles.btnActive : {}) }}
          onClick={() => castVote("a")}
          disabled={!!voted || loading}
        >
          {votes.option_a}
          {voted && <span style={styles.pct}> {pctA}%</span>}
        </button>

        <button
          style={{ ...styles.btn, ...(voted === "b" ? styles.btnActive : {}) }}
          onClick={() => castVote("b")}
          disabled={!!voted || loading}
        >
          {votes.option_b}
          {voted && <span style={styles.pct}> {pctB}%</span>}
        </button>
      </div>

      {voted && (
        <p style={styles.thanks}>
          Voted! Results: {votes.votes_a} vs {votes.votes_b} — updating the board…
        </p>
      )}
    </main>
  );
}

const styles: Record<string, React.CSSProperties> = {
  main: {
    display: "flex", flexDirection: "column", alignItems: "center",
    justifyContent: "center", minHeight: "100vh", padding: "2rem", gap: "1.5rem",
  },
  title: { fontSize: "2rem", margin: 0, letterSpacing: "0.05em" },
  question: { fontSize: "1.4rem", textAlign: "center", maxWidth: "400px" },
  buttons: { display: "flex", gap: "1.5rem", flexWrap: "wrap", justifyContent: "center" },
  btn: {
    padding: "1rem 2rem", fontSize: "1.2rem", borderRadius: "8px",
    border: "2px solid #555", background: "#222", color: "#fff",
    cursor: "pointer", transition: "all 0.15s",
    minWidth: "140px",
  },
  btnActive: { border: "2px solid #4af", background: "#1a3a4a" },
  pct: { fontWeight: "bold", color: "#4af" },
  thanks: { color: "#8f8", fontSize: "0.95rem", textAlign: "center" },
};
