"use client";

import { formatUptime } from "@/lib/format";
import type { Proc, Snapshot } from "@/lib/types";
import { useApi } from "@/lib/useApi";

/** Live view of the host itself. Admin only: the backend refuses these calls for user keys. */
export default function LiveHost({ auto }: { auto: boolean }) {
  const snap = useApi<Snapshot>("system", auto ? 15000 : 0);
  const procs = useApi<Proc[]>("system/processes?limit=8&sort_by=cpu_percent", auto ? 15000 : 0);

  if (snap.error) return <p className="err">Live host data unavailable: {snap.error}</p>;
  const s = snap.data;
  if (!s) return <p className="muted">Loading host...</p>;

  return (
    <div className="grid two">
      <section className="card">
        <h2>
          {s.host.hostname} <span className="meta">up {formatUptime(s.host.uptime_seconds)}</span>
        </h2>
        <p className="meta">{s.host.platform}</p>
        <table>
          <thead>
            <tr>
              <th>Disk</th>
              <th>Usage</th>
              <th className="num">Used / total</th>
            </tr>
          </thead>
          <tbody>
            {s.disks.map((d) => (
              <tr key={d.mountpoint}>
                <td>{d.mountpoint}</td>
                <td>
                  <div className="bar" role="img" aria-label={`${d.usage_percent}% used`}>
                    <i style={{ width: `${Math.min(100, d.usage_percent)}%` }} />
                  </div>
                </td>
                <td className="num">
                  {d.usage_percent.toFixed(0)}% · {d.used_gib.toFixed(0)}/{d.total_gib.toFixed(0)} GiB
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        <p className="meta">
          Memory {s.memory.used_gib.toFixed(1)}/{s.memory.total_gib.toFixed(1)} GiB · swap {s.memory.swap_percent}% ·{" "}
          {s.network.connections ?? "?"} connections
        </p>
      </section>

      <section className="card">
        <h2>Top processes by CPU</h2>
        <div className="scroll">
          <table>
            <thead>
              <tr>
                <th>Process</th>
                <th className="num">PID</th>
                <th className="num">CPU</th>
                <th className="num">Mem</th>
              </tr>
            </thead>
            <tbody>
              {(procs.data ?? []).map((p) => (
                <tr key={p.pid}>
                  <td>{p.name ?? "?"}</td>
                  <td className="num">{p.pid}</td>
                  <td className="num">{p.cpu_percent?.toFixed(1) ?? "-"}%</td>
                  <td className="num">{p.memory_percent?.toFixed(1) ?? "-"}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
