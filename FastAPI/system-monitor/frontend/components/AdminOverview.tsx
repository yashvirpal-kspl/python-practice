"use client";

import { formatAgo } from "@/lib/format";
import type { Overview, OverviewItem } from "@/lib/types";

const STATUS: Record<OverviewItem["status"], { icon: string; label: string }> = {
  ok: { icon: "✔", label: "Up" },
  down: { icon: "✖", label: "Down" },
  pending: { icon: "•", label: "Waiting for first sample" },
  disabled: { icon: "–", label: "Disabled" },
};

const pct = (v: number | null) => (v == null ? "-" : `${v.toFixed(0)}%`);
export const itemValue = (i: OverviewItem) => `${i.user_id}/${i.name}`;

interface Props {
  data: Overview | null;
  selected: string;
  onSelect: (value: string) => void;
}

/** Admin-only: every monitored server across all users, with latest metrics. */
export default function AdminOverview({ data, selected, onSelect }: Props) {
  if (!data) return <p className="muted">Loading servers...</p>;
  const down = data.items.filter((i) => i.status === "down").length;

  return (
    <>
      <div className="grid stats">
        <div className="card stat">
          <div className="label">Users</div>
          <div className="value">{data.users}</div>
        </div>
        <div className="card stat">
          <div className="label">Monitored servers</div>
          <div className="value">{data.servers}</div>
        </div>
        <div className="card stat">
          <div className="label">Servers down</div>
          <div className="value">
            {down > 0 && <span className="st down" aria-hidden>{"✖ "}</span>}
            {down}
          </div>
        </div>
      </div>

      <section className="card">
        <h2>All servers</h2>
        <div className="scroll">
          <table>
            <thead>
              <tr>
                <th>Server</th>
                <th>Owner</th>
                <th>Status</th>
                <th className="num">CPU</th>
                <th className="num">Memory</th>
                <th className="num">Disk</th>
                <th>Last seen</th>
                <th />
              </tr>
            </thead>
            <tbody>
              {data.items.map((i) => {
                const v = itemValue(i);
                const st = STATUS[i.status];
                return (
                  <tr key={v} className={v === selected ? "selected" : undefined}>
                    <td>
                      <strong>{i.name}</strong>
                      {i.url && <div className="url">{i.url}</div>}
                    </td>
                    <td>{i.is_host ? "this host" : (i.owner_email ?? "admin")}</td>
                    <td>
                      <span className={`st ${i.status}`}>
                        <span aria-hidden>{st.icon}</span> {st.label}
                      </span>
                    </td>
                    <td className="num">{pct(i.cpu)}</td>
                    <td className="num">{pct(i.mem)}</td>
                    <td className="num">{pct(i.disk)}</td>
                    <td>{i.last_seen ? formatAgo(i.last_seen) : "-"}</td>
                    <td>
                      <button className="btn small" onClick={() => onSelect(v)} aria-pressed={v === selected}>
                        {v === selected ? "Viewing" : "View charts"}
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </section>
    </>
  );
}
