import { NextResponse } from "next/server";
import { readVotes } from "@/lib/github";

export async function GET() {
  try {
    const { data } = await readVotes();
    return NextResponse.json(data);
  } catch (e: unknown) {
    const message = e instanceof Error ? e.message : "Unknown error";
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
