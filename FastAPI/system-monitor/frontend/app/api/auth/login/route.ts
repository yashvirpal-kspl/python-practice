import { NextResponse } from "next/server";
import { BACKEND, COOKIE, cookieOptions } from "@/lib/server";

export async function POST(req: Request) {
  const body = await req.json().catch(() => null);
  const key = typeof body?.api_key === "string" ? body.api_key.trim() : "";
  if (!key) return NextResponse.json({ detail: "API key is required" }, { status: 400 });

  // Validate the key against the backend before storing it
  const res = await fetch(`${BACKEND}/me`, { headers: { "X-API-Key": key }, cache: "no-store" }).catch(() => null);
  if (!res) return NextResponse.json({ detail: "Cannot reach the monitor backend" }, { status: 502 });
  if (!res.ok) return NextResponse.json({ detail: "Invalid API key" }, { status: 401 });

  const out = NextResponse.json(await res.json());
  out.cookies.set(COOKIE, key, cookieOptions());
  return out;
}
