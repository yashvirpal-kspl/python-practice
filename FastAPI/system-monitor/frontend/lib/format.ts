import type { Row, Sample } from "./types";

export const RANGES = [
  { label: "15 min", minutes: 15 },
  { label: "1 hour", minutes: 60 },
  { label: "6 hours", minutes: 360 },
  { label: "24 hours", minutes: 1440 },
  { label: "7 days", minutes: 10080 },
] as const;

const MAX_POINTS = 240;

const orNull = (v: number | null | undefined) => (typeof v === "number" ? v : null);

/** Samples -> chart rows. Network counters are cumulative, so convert them to KB/s. */
export function toRows(samples: Sample[]): Row[] {
  return samples.map((s, i) => {
    const prev = samples[i - 1];
    let netIn: number | null = null;
    let netOut: number | null = null;
    if (prev) {
      const dt = s.ts - prev.ts;
      if (dt > 0 && s.net_recv_mb != null && prev.net_recv_mb != null) {
        const r = ((s.net_recv_mb - prev.net_recv_mb) / dt) * 1024;
        netIn = r >= 0 ? r : null; // negative = counter reset after a reboot
      }
      if (dt > 0 && s.net_sent_mb != null && prev.net_sent_mb != null) {
        const o = ((s.net_sent_mb - prev.net_sent_mb) / dt) * 1024;
        netOut = o >= 0 ? o : null;
      }
    }
    return {
      t: s.ts * 1000,
      cpu: orNull(s.cpu),
      mem: orNull(s.mem),
      disk: orNull(s.disk),
      load: orNull(s.load1),
      netIn,
      netOut,
    };
  });
}

/** Average into at most MAX_POINTS buckets so long ranges stay fast and readable. */
export function bucket(rows: Row[]): Row[] {
  if (rows.length <= MAX_POINTS) return rows;
  const size = Math.ceil(rows.length / MAX_POINTS);
  const keys = ["cpu", "mem", "disk", "load", "netIn", "netOut"] as const;
  const out: Row[] = [];
  for (let i = 0; i < rows.length; i += size) {
    const chunk = rows.slice(i, i + size);
    const row = { t: chunk[Math.floor(chunk.length / 2)].t } as Row;
    for (const k of keys) {
      const vals = chunk.map((r) => r[k]).filter((v): v is number => v != null);
      row[k] = vals.length ? vals.reduce((a, b) => a + b, 0) / vals.length : null;
    }
    out.push(row);
  }
  return out;
}

export function formatTick(t: number, rangeMinutes: number): string {
  const d = new Date(t);
  const time = d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  if (rangeMinutes <= 1440) return time;
  return `${d.toLocaleDateString([], { month: "short", day: "numeric" })} ${time}`;
}

export function formatFull(t: number): string {
  return new Date(t).toLocaleString([], {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });
}

export function formatAgo(tsSeconds: number): string {
  const s = Math.max(0, Math.round(Date.now() / 1000 - tsSeconds));
  if (s < 60) return `${s}s ago`;
  if (s < 3600) return `${Math.floor(s / 60)}m ago`;
  if (s < 86400) return `${Math.floor(s / 3600)}h ago`;
  return `${Math.floor(s / 86400)}d ago`;
}

export function formatUptime(seconds: number): string {
  const d = Math.floor(seconds / 86400);
  const h = Math.floor((seconds % 86400) / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  return d ? `${d}d ${h}h` : h ? `${h}h ${m}m` : `${m}m`;
}

export function formatRate(kbps: number): string {
  return kbps >= 1024 ? `${(kbps / 1024).toFixed(2)} MB/s` : `${kbps.toFixed(1)} KB/s`;
}
