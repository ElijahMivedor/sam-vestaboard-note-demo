import { NextRequest, NextResponse } from "next/server";
import { readVotes, writeVotes } from "@/lib/github";
import { triggerVoteUpdate } from "@/lib/vestaboard";

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const side = body?.side;
    if (side !== "a" && side !== "b") {
      return NextResponse.json({ error: 'side must be "a" or "b"' }, { status: 400 });
    }

    const { data, sha } = await readVotes();

    if (side === "a") {
      data.votes_a += 1;
    } else {
      data.votes_b += 1;
    }

    await writeVotes(data, sha, `vote: +1 for ${side === "a" ? data.option_a : data.option_b}`);

    // Fire workflow_dispatch — non-blocking, ignore failures so vote still registers
    triggerVoteUpdate().catch((e) => console.error("workflow_dispatch failed:", e));

    return NextResponse.json(data);
  } catch (e: unknown) {
    const message = e instanceof Error ? e.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
