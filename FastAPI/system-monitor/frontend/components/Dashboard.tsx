"use client";

import { useRouter } from "next/navigation";
import { useEffect, useMemo, useState } from "react";
import AdminOverview, { itemValue } from "./AdminOverview";
import AlertsPanel from "./AlertsPanel";
import LiveHost from "./LiveHost";
import MetricChart from "./MetricChart";
import SamplesTable from "./SamplesTable";
import ServersPanel from "./ServersPanel";
import { bucket, formatAgo, formatRate, RANGES, toRows } from "@/lib/format";
import type { AlertRecord, Me, Overview, Sample, Server } from "@/lib/types";
import { useApi } from "@/lib/useApi";

const pct = (v: number) => `${Math.round(v * 10) / 10}%`;
const num = (v: number) => `${Math.round(v * 100) / 100}`;

export default function Dashboard() {
  const router = useRouter();
  const [auto, setAuto] = useState(true);
  const [range, setRange] = useState<number>(60);
  // Users: a server name. Admin: "<user_id>/<server name>" (see itemValue)
  const [node, setNode] = useState("");
  const [table, setTable] = useState(false);
  const interval = auto ? 30000 : 0;

  const me = useApi<Me>("me");
  const isAdmin = me.data?.is_admin === true;
  const ready = me.data !== null;

  const overview = useApi<Overview>(isAdmin ? "admin/overview" : null, interval);
  const nodes = useApi<string[]>(ready && !isAdmin ? "history/nodes" : null, interval);
  const servers = useApi<Server[]>("servers");
  const alerts = useApi<AlertRecord[]>(
    ready ? (isAdmin ? "admin/alerts?limit=20" : "alerts?limit=20") : null,
    interval,
  );

  const options = useMemo(
    () =>
      isAdmin
        ? (overview.data?.items ?? []).map((i) => ({
            value: itemValue(i),
            label: i.is_host ? `${i.name} (this host)` : `${i.owner_email ?? "admin"} · ${i.name}`,
          }))
        : (nodes.data ?? []).map((n) => ({ value: n, label: n })),
    [isAdmin, overview.data, nodes.data],
  );

  // Default to the first server; recover if the selected one disappears
  useEffect(() => {
    if (options.length && !options.some((o) => o.value === node)) setNode(options[0].value);
  }, [options, node]);

  let historyPath: string | null = null;
  if (node) {
    if (isAdmin) {
      const slash = node.indexOf("/");
      if (slash > 0) {
        const uid = node.slice(0, slash);
        const name = node.slice(slash + 1);
        historyPath = `admin/history?user_id=${uid}&node=${encodeURIComponent(name)}&minutes=${range}&limit=5000`;
      }
    } else {
      historyPath = `history?node=${encodeURIComponent(node)}&minutes=${range}&limit=5000`;
    }
  }
  const history = useApi<Sample[]>(historyPath, interval);

  const rows = useMemo(() => bucket(toRows(history.data ?? [])), [history.data]);
  const latest = history.data?.length ? history.data[history.data.length - 1] : null;
  const stale = history.loading;

  async function logout() {
    await fetch("/api/auth/logout", { method: "POST" });
    router.push("/login");
  }

  function refreshAll() {
    overview.reload();
    nodes.reload();
    servers.reload();
    alerts.reload();
    history.reload();
  }

  const noServers = !isAdmin && nodes.data !== null && nodes.data.length === 0;

  return (
    <div className="wrap">
      <header className="topbar">
        <span className="brand">VPS Monitor</span>
        <div className="who">
          {me.data && (
            <>
              <span>{me.data.email ?? "Admin"}</span>
              {isAdmin && <span className="badge">admin</span>}
            </>
          )}
          <button className="btn small" onClick={logout}>
            Sign out
          </button>
        </div>
      </header>

      {isAdmin && (
        <>
          <div className="section-title">
            <h2>All servers</h2>
          </div>
          {overview.error && <p className="err">Could not load servers: {overview.error}</p>}
          <AdminOverview data={overview.data} selected={node} onSelect={setNode} />

          <div className="section-title">
            <h2>This host (live)</h2>
          </div>
          <LiveHost auto={auto} />
        </>
      )}

      <div className="section-title">
        <h2>History</h2>
      </div>

      {/* One filter row above everything it scopes */}
      <div className="filters">
        <label>
          <span className="meta">Server </span>
          <select className="input" value={node} onChange={(e) => setNode(e.target.value)} disabled={!options.length}>
            {options.map((o) => (
              <option key={o.value} value={o.value}>
                {o.label}
              </option>
            ))}
          </select>
        </label>
        <div className="seg" role="group" aria-label="Time range">
          {RANGES.map((r) => (
            <button key={r.minutes} aria-pressed={range === r.minutes} onClick={() => setRange(r.minutes)}>
              {r.label}
            </button>
          ))}
        </div>
        <label className="check">
          <input type="checkbox" checked={auto} onChange={(e) => setAuto(e.target.checked)} />
          Auto-refresh
        </label>
        <button className="btn small" onClick={refreshAll}>
          Refresh
        </button>
        <label className="check">
          <input type="checkbox" checked={table} onChange={(e) => setTable(e.target.checked)} />
          Table view
        </label>
      </div>

      {history.error && <p className="err">Could not load history: {history.error}</p>}

      {noServers ? (
        <section className="card">
          <h2>No data yet</h2>
          <p className="muted">
            Add a server below. Once the monitor has polled it (every minute by default) its charts appear here.
          </p>
        </section>
      ) : (
        <>
          <div className="grid stats">
            <Stat label="CPU" value={latest?.cpu} unit="%" />
            <Stat label="Memory" value={latest?.mem} unit="%" />
            <Stat label="Disk (fullest)" value={latest?.disk} unit="%" />
            <Stat label="Load (1 min)" value={latest?.load1} unit="" digits={2} />
            <div className="card stat">
              <div className="label">Last sample</div>
              <div className="value" style={{ fontSize: 20 }}>
                {latest ? formatAgo(latest.ts) : "-"}
              </div>
            </div>
          </div>

          {table ? (
            <SamplesTable rows={rows} />
          ) : (
            <div className="grid charts">
              <MetricChart title="CPU usage" series={[{ key: "cpu", label: "CPU", color: "var(--c-cpu)" }]}
                rows={rows} rangeMinutes={range} fmt={pct} domain={[0, 100]} stale={stale} />
              <MetricChart title="Memory usage" series={[{ key: "mem", label: "Memory", color: "var(--c-mem)" }]}
                rows={rows} rangeMinutes={range} fmt={pct} domain={[0, 100]} stale={stale} />
              <MetricChart title="Disk usage (fullest partition)" series={[{ key: "disk", label: "Disk", color: "var(--c-disk)" }]}
                rows={rows} rangeMinutes={range} fmt={pct} domain={[0, 100]} stale={stale} />
              <MetricChart title="Load average (1 min)" series={[{ key: "load", label: "Load", color: "var(--c-load)" }]}
                rows={rows} rangeMinutes={range} fmt={num} stale={stale} />
              <MetricChart title="Network throughput"
                series={[
                  { key: "netIn", label: "In", color: "var(--c-in)" },
                  { key: "netOut", label: "Out", color: "var(--c-out)" },
                ]}
                rows={rows} rangeMinutes={range} fmt={formatRate} stale={stale} />
            </div>
          )}
          {history.data?.length === 0 && !history.loading && node && (
            <p className="muted">No samples for this server in this range yet.</p>
          )}
        </>
      )}

      <div className="grid two">
        <ServersPanel servers={servers.data ?? []} onChange={refreshAll} />
        <AlertsPanel alerts={alerts.data ?? []} />
      </div>
    </div>
  );
}

function Stat({ label, value, unit, digits = 1 }: { label: string; value?: number | null; unit: string; digits?: number }) {
  return (
    <div className="card stat">
      <div className="label">{label}</div>
      <div className="value">
        {value == null ? "-" : value.toFixed(digits)}
        {value != null && unit && <small>{unit}</small>}
      </div>
    </div>
  );
}
