"use client";

import { FormEvent, useState } from "react";
import { api } from "@/lib/api";
import type { Server } from "@/lib/types";

interface Props {
  servers: Server[];
  onChange: () => void;
}

export default function ServersPanel({ servers, onChange }: Props) {
  const [name, setName] = useState("");
  const [url, setUrl] = useState("");
  const [key, setKey] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function add(e: FormEvent) {
    e.preventDefault();
    setBusy(true);
    setError(null);
    try {
      await api("servers", { method: "POST", body: JSON.stringify({ name, url, api_key: key }) });
      setName("");
      setUrl("");
      setKey("");
      onChange();
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setBusy(false);
    }
  }

  async function remove(n: string) {
    if (!window.confirm(`Stop monitoring "${n}"? Its stored history stays until it expires.`)) return;
    try {
      await api(`servers/${encodeURIComponent(n)}`, { method: "DELETE" });
      onChange();
    } catch (err) {
      setError((err as Error).message);
    }
  }

  return (
    <section className="card">
      <h2>Servers</h2>
      {servers.length > 0 && (
        <ul className="list">
          {servers.map((s) => (
            <li key={s.id}>
              <div style={{ flex: 1, minWidth: 0 }}>
                <strong>{s.name}</strong>
                <div className="meta" style={{ overflowWrap: "anywhere" }}>
                  {s.url}
                </div>
              </div>
              <button className="btn small danger" onClick={() => remove(s.name)}>
                Remove
              </button>
            </li>
          ))}
        </ul>
      )}

      <form className="form" onSubmit={add}>
        <input
          className="input"
          placeholder="Name (letters, digits . _ -)"
          value={name}
          onChange={(e) => setName(e.target.value)}
          pattern="[A-Za-z0-9._\-]{1,40}"
          required
        />
        <input
          className="input"
          placeholder="https://your-server.example.com"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          type="url"
          required
        />
        <input
          className="input"
          placeholder="That server's API key"
          value={key}
          onChange={(e) => setKey(e.target.value)}
          type="password"
          autoComplete="off"
        />
        <button className="btn primary" disabled={busy}>
          {busy ? "Adding..." : "Add server"}
        </button>
        {error && <p className="err">{error}</p>}
      </form>
    </section>
  );
}
