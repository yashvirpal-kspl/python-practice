import { NextResponse } from "next/server";
import { BACKEND, COOKIE, cookieOptions, forwardedFor } from "@/lib/server";

export async function POST(req: Request) {
  const res = await fetch(`${BACKEND}/users/verify`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...forwardedFor(req) },
    body: await req.text(),
    cache: "no-store",
  }).catch(() => null);
  if (!res) return NextResponse.json({ detail: "Cannot reach the monitor backend" }, { status: 502 });

  const data = await res.json().catch(() => ({}));
  const out = NextResponse.json(data, { status: res.status });
  if (res.ok && data.api_key) {
    // Sign the user in; the key is also returned once so they can save it for scripts
    out.cookies.set(COOKIE, data.api_key, cookieOptions());
  }
  return out;
}
