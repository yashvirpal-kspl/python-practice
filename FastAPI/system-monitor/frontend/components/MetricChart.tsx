"use client";

import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { formatFull, formatTick } from "@/lib/format";
import type { Row } from "@/lib/types";

export interface Series {
  key: keyof Row;
  label: string;
  color: string; // CSS var, e.g. "var(--c-cpu)"
}

interface Props {
  title: string;
  series: Series[];
  rows: Row[];
  rangeMinutes: number;
  fmt: (v: number) => string;
  domain?: [number, number];
  stale?: boolean;
}

interface TipProps {
  active?: boolean;
  payload?: { dataKey: string; value: number | null }[];
  label?: number;
  series: Series[];
  fmt: (v: number) => string;
}

// Values lead, series names follow; rows are keyed with a short line, not a box.
function ChartTooltip({ active, payload, label, series, fmt }: TipProps) {
  if (!active || !payload?.length || label == null) return null;
  return (
    <div className="tooltip">
      <div className="when">{formatFull(label)}</div>
      {series.map((s) => {
        const v = payload.find((p) => p.dataKey === s.key)?.value;
        return (
          <div className="row" key={s.key}>
            <i className="key" style={{ borderColor: s.color, margin: 0 }} />
            <strong>{v == null ? "no data" : fmt(v)}</strong>
            <span>{s.label}</span>
          </div>
        );
      })}
    </div>
  );
}

export default function MetricChart({ title, series, rows, rangeMinutes, fmt, domain, stale }: Props) {
  const last = rows.length ? rows[rows.length - 1] : null;
  const now = last && series.length === 1 ? (last[series[0].key] as number | null) : null;

  return (
    <section className="card" aria-label={title}>
      <div className="chart-head">
        <h2>{title}</h2>
        {series.length === 1 && <span className="now">{now == null ? "-" : fmt(now)}</span>}
      </div>

      {series.length > 1 && (
        <div className="legend">
          {series.map((s) => {
            const v = last ? (last[s.key] as number | null) : null;
            return (
              <span key={s.key}>
                <i className="key" style={{ borderColor: s.color }} />
                {s.label}
                {v != null ? ` ${fmt(v)}` : ""}
              </span>
            );
          })}
        </div>
      )}

      <div className={`chart-body${stale ? " stale" : ""}`} style={{ height: 200 }}>
        {rows.length < 2 ? (
          <div className="empty">Not enough data yet</div>
        ) : (
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={rows} margin={{ top: 6, right: 8, bottom: 0, left: 0 }}>
              <CartesianGrid vertical={false} stroke="var(--grid)" />
              <XAxis
                dataKey="t"
                type="number"
                scale="time"
                domain={["dataMin", "dataMax"]}
                tickFormatter={(t: number) => formatTick(t, rangeMinutes)}
                tick={{ fill: "var(--ink-muted)", fontSize: 11 }}
                stroke="var(--axis)"
                tickLine={false}
                minTickGap={48}
              />
              <YAxis
                domain={domain ?? [0, "auto"]}
                tickFormatter={(v: number) => fmt(v)}
                tick={{ fill: "var(--ink-muted)", fontSize: 11 }}
                axisLine={false}
                tickLine={false}
                width={68}
              />
              <Tooltip
                cursor={{ stroke: "var(--ink-muted)", strokeWidth: 1 }}
                content={<ChartTooltip series={series} fmt={fmt} />}
                isAnimationActive={false}
              />
              {series.map((s) => (
                <Line
                  key={s.key}
                  type="monotone"
                  dataKey={s.key}
                  name={s.label}
                  stroke={s.color}
                  strokeWidth={2}
                  dot={false}
                  activeDot={{ r: 4, stroke: "var(--surface)", strokeWidth: 2, fill: s.color }}
                  connectNulls={false}
                  isAnimationActive={false}
                />
              ))}
            </LineChart>
          </ResponsiveContainer>
        )}
      </div>
    </section>
  );
}
