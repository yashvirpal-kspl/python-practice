import { cookies } from "next/headers";
import { NextResponse } from "next/server";
import { BACKEND, COOKIE, cookieOptions } from "@/lib/server";

export async function POST() {
  const key = (await cookies()).get(COOKIE)?.value;
  // Admin sessions are ended on the backend too, so the token is dead even if it leaked
  if (key?.startsWith("vpsm_s_")) {
    await fetch(`${BACKEND}/auth/logout`, { method: "POST", headers: { "X-API-Key": key }, cache: "no-store" }).catch(
      () => null,
    );
  }
  const out = NextResponse.json({ ok: true });
  out.cookies.set(COOKIE, "", { ...cookieOptions(), maxAge: 0 });
  return out;
}
