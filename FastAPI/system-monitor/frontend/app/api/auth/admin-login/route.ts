import { NextResponse } from "next/server";
import { BACKEND, COOKIE, cookieOptions, forwardedFor } from "@/lib/server";

export async function POST(req: Request) {
  const res = await fetch(`${BACKEND}/auth/admin/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...forwardedFor(req) },
    body: await req.text(),
    cache: "no-store",
  }).catch(() => null);
  if (!res) return NextResponse.json({ detail: "Cannot reach the monitor backend" }, { status: 502 });

  const data = await res.json().catch(() => ({}));
  if (!res.ok) return NextResponse.json(data, { status: res.status });

  // The session token goes straight into an httpOnly cookie; the browser never receives it
  const out = NextResponse.json({ ok: true });
  out.cookies.set(COOKIE, data.token, cookieOptions(data.expires_in));
  return out;
}
