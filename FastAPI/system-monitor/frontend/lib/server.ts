// Server-only helpers shared by the route handlers.
export const BACKEND = (process.env.BACKEND_URL ?? "http://127.0.0.1:8000").replace(/\/$/, "");
export const COOKIE = "vpsm_key";

export function cookieOptions(maxAgeSeconds = 60 * 60 * 24 * 30) {
  // An empty COOKIE_SECURE (e.g. passed through docker compose) counts as unset
  const override = process.env.COOKIE_SECURE;
  const secure = override ? override === "true" : process.env.NODE_ENV === "production";
  return {
    httpOnly: true, // the key is never readable from page JavaScript
    sameSite: "lax" as const, // blocks cross-site POST/DELETE carrying the cookie
    secure,
    path: "/",
    maxAge: maxAgeSeconds,
  };
}

/** Forward the visitor's IP so the backend's per-IP sign-up limit sees real clients. */
export function forwardedFor(req: Request): Record<string, string> {
  const xff = req.headers.get("x-forwarded-for");
  return xff ? { "x-forwarded-for": xff } : {};
}
