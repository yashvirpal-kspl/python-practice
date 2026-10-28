"use client";

import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";
import { errorDetail } from "@/lib/api";

type Mode = "key" | "signup" | "admin";
type Step = "email" | "code" | "done";

async function post(path: string, body: unknown) {
  const res = await fetch(path, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(await errorDetail(res));
  return res.json();
}

export default function LoginPage() {
  const router = useRouter();
  const [mode, setMode] = useState<Mode>("key");
  const [step, setStep] = useState<Step>("email");
  const [apiKey, setApiKey] = useState("");
  const [email, setEmail] = useState("");
  const [code, setCode] = useState("");
  const [adminEmail, setAdminEmail] = useState("");
  const [adminPassword, setAdminPassword] = useState("");
  const [newKey, setNewKey] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [info, setInfo] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function run(fn: () => Promise<void>) {
    setBusy(true);
    setError(null);
    setInfo(null);
    try {
      await fn();
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }

  const pick = (m: Mode) => {
    setMode(m);
    setError(null);
    setInfo(null);
  };

  const signIn = (e: FormEvent) => {
    e.preventDefault();
    run(async () => {
      await post("/api/auth/login", { api_key: apiKey });
      router.push("/dashboard");
    });
  };

  const adminSignIn = (e: FormEvent) => {
    e.preventDefault();
    run(async () => {
      await post("/api/auth/admin-login", { email: adminEmail, password: adminPassword });
      setAdminPassword("");
      router.push("/dashboard");
    });
  };

  const requestCode = (e: FormEvent) => {
    e.preventDefault();
    run(async () => {
      await post("/api/auth/register", { email });
      setStep("code");
      setInfo("If the address is valid, a verification code is on its way. It expires in 30 minutes.");
    });
  };

  const verify = (e: FormEvent) => {
    e.preventDefault();
    run(async () => {
      const r = await post("/api/auth/verify", { email, code: code.trim() });
      setNewKey(r.api_key);
      setStep("done");
    });
  };

  return (
    <main className="login">
      <div className="card">
        <h1 style={{ fontSize: 20 }}>VPS Monitor</h1>
        <p className="muted">Sign in with your API key, create an account with your email, or sign in as admin.</p>

        <div className="tabs" role="tablist">
          <div className="seg">
            <button aria-pressed={mode === "key"} onClick={() => pick("key")}>
              API key
            </button>
            <button aria-pressed={mode === "signup"} onClick={() => pick("signup")}>
              Create or recover
            </button>
            <button aria-pressed={mode === "admin"} onClick={() => pick("admin")}>
              Admin
            </button>
          </div>
        </div>

        {mode === "key" && (
          <form className="form" onSubmit={signIn}>
            <input
              className="input"
              type="password"
              placeholder="API key"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              autoComplete="current-password"
              required
            />
            <button className="btn primary" disabled={busy}>
              {busy ? "Checking..." : "Sign in"}
            </button>
          </form>
        )}

        {mode === "admin" && (
          <form className="form" onSubmit={adminSignIn}>
            <input
              className="input"
              type="email"
              placeholder="Admin email"
              value={adminEmail}
              onChange={(e) => setAdminEmail(e.target.value)}
              autoComplete="username"
              required
            />
            <input
              className="input"
              type="password"
              placeholder="Password"
              value={adminPassword}
              onChange={(e) => setAdminPassword(e.target.value)}
              autoComplete="current-password"
              required
            />
            <button className="btn primary" disabled={busy}>
              {busy ? "Signing in..." : "Sign in as admin"}
            </button>
            <p className="meta">
              Admins see every user&apos;s servers. After repeated wrong passwords this address is locked out for a while.
            </p>
          </form>
        )}

        {mode === "signup" && step === "email" && (
          <form className="form" onSubmit={requestCode}>
            <input
              className="input"
              type="email"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              autoComplete="email"
              required
            />
            <button className="btn primary" disabled={busy}>
              {busy ? "Sending..." : "Email me a code"}
            </button>
            <p className="meta">
              Already registered? This sends a code that issues a new key and replaces the old one.
            </p>
          </form>
        )}

        {mode === "signup" && step === "code" && (
          <form className="form" onSubmit={verify}>
            <input
              className="input"
              placeholder="Verification code"
              value={code}
              onChange={(e) => setCode(e.target.value)}
              autoComplete="one-time-code"
              required
            />
            <button className="btn primary" disabled={busy}>
              {busy ? "Verifying..." : "Verify"}
            </button>
            <button type="button" className="btn small" onClick={() => setStep("email")}>
              Use a different email
            </button>
          </form>
        )}

        {mode === "signup" && step === "done" && (
          <div>
            <p className="ok">You are signed in. Your API key:</p>
            <div className="keybox">{newKey}</div>
            <p className="meta">
              Save it now (for scripts or signing in elsewhere). It is shown only once and cannot be recovered, only replaced.
            </p>
            <div className="row-between" style={{ marginTop: 8 }}>
              <button className="btn" onClick={() => navigator.clipboard?.writeText(newKey)}>
                Copy key
              </button>
              <button className="btn primary" onClick={() => router.push("/dashboard")}>
                Continue to dashboard
              </button>
            </div>
          </div>
        )}

        {info && <p className="ok">{info}</p>}
        {error && <p className="err">{error}</p>}
      </div>
    </main>
  );
}
