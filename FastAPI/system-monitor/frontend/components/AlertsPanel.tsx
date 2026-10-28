"use client";

import { useState } from "react";
import { api } from "@/lib/api";
import { formatAgo } from "@/lib/format";
import type { AlertRecord } from "@/lib/types";

const ICON: Record<string, string> = { critical: "✖", warning: "▲", resolved: "✔" };

export default function AlertsPanel({ alerts }: { alerts: AlertRecord[] }) {
  const [msg, setMsg] = useState<{ ok: boolean; text: string } | null>(null);
  const [busy, setBusy] = useState(false);

  async function sendTest() {
    setBusy(true);
    setMsg(null);
    try {
      const r = await api<{ sent_to: string[] }>("alerts/test", { method: "POST" });
      setMsg({ ok: true, text: `Test email sent to ${r.sent_to.join(", ")}` });
    } catch (e) {
      setMsg({ ok: false, text: (e as Error).message });
    } finally {
      setBusy(false);
    }
  }

  return (
    <section className="card">
      <div className="row-between">
        <h2>Alerts</h2>
        <button className="btn small" onClick={sendTest} disabled={busy}>
          Send test email
        </button>
      </div>
      {msg && <p className={msg.ok ? "ok" : "err"}>{msg.text}</p>}
      {alerts.length === 0 ? (
        <p className="muted">No alerts. Emails are sent when a server crosses a threshold or stops responding.</p>
      ) : (
        <ul className="list">
          {alerts.map((a) => (
            <li key={a.id}>
              <span className={`lvl ${a.level}`}>
                <span className="ic" aria-hidden>
                  {ICON[a.level] ?? "•"}
                </span>{" "}
                {a.level}
              </span>
              <div>
                <div>
                  <strong>{a.node}</strong>
                  {a.owner_email ? <span className="meta"> ({a.owner_email})</span> : null}: {a.message}
                </div>
                <div className="meta">
                  {formatAgo(a.ts)} · {a.emailed ? "emailed" : "not emailed"}
                </div>
              </div>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
