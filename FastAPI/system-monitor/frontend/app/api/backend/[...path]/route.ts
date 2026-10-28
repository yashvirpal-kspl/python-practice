import { cookies } from "next/headers";
import { NextRequest, NextResponse } from "next/server";
import { BACKEND, COOKIE } from "@/lib/server";

// Only these backend areas are reachable through the proxy.
const ALLOWED = new Set(["me", "servers", "history", "alerts", "system", "files", "admin"]);

async function proxy(req: NextRequest, ctx: { params: Promise<{ path: string[] }> }) {
  const { path } = await ctx.params;
  if (!ALLOWED.has(path[0]) || path.some((p) => p === ".." || p === ".")) {
    return NextResponse.json({ detail: "Not found" }, { status: 404 });
  }

  const key = (await cookies()).get(COOKIE)?.value;
  if (!key) return NextResponse.json({ detail: "Not authenticated" }, { status: 401 });

  const hasBody = req.method !== "GET" && req.method !== "HEAD";
  const res = await fetch(`${BACKEND}/${path.map(encodeURIComponent).join("/")}${req.nextUrl.search}`, {
    method: req.method,
    headers: { "X-API-Key": key, "Content-Type": "application/json" },
    body: hasBody ? await req.text() : undefined,
    cache: "no-store",
  }).catch(() => null);
  if (!res) return NextResponse.json({ detail: "Cannot reach the monitor backend" }, { status: 502 });

  return new NextResponse(res.status === 204 ? null : res.body, {
    status: res.status,
    headers: { "Content-Type": res.headers.get("content-type") ?? "application/json" },
  });
}

export { proxy as GET, proxy as POST, proxy as DELETE };
