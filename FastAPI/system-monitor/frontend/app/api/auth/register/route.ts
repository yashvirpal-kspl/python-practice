import { NextResponse } from "next/server";
import { BACKEND, forwardedFor } from "@/lib/server";

export async function POST(req: Request) {
  const body = await req.text();
  const res = await fetch(`${BACKEND}/users/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...forwardedFor(req) },
    body,
    cache: "no-store",
  }).catch(() => null);
  if (!res) return NextResponse.json({ detail: "Cannot reach the monitor backend" }, { status: 502 });
  return new NextResponse(await res.text(), {
    status: res.status,
    headers: { "Content-Type": "application/json" },
  });
}
