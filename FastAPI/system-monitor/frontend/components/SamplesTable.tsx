import { formatFull, formatRate } from "@/lib/format";
import type { Row } from "@/lib/types";

const pct = (v: number | null) => (v == null ? "-" : `${v.toFixed(1)}%`);

/** Table view of the same rows the charts plot, newest first. */
export default function SamplesTable({ rows }: { rows: Row[] }) {
  const shown = [...rows].reverse().slice(0, 200);
  return (
    <section className="card">
      <h2>Samples (newest first, up to 200)</h2>
      <div className="scroll">
        <table>
          <thead>
            <tr>
              <th>Time</th>
              <th className="num">CPU</th>
              <th className="num">Memory</th>
              <th className="num">Disk</th>
              <th className="num">Load (1m)</th>
              <th className="num">Net in</th>
              <th className="num">Net out</th>
            </tr>
          </thead>
          <tbody>
            {shown.map((r) => (
              <tr key={r.t}>
                <td>{formatFull(r.t)}</td>
                <td className="num">{pct(r.cpu)}</td>
                <td className="num">{pct(r.mem)}</td>
                <td className="num">{pct(r.disk)}</td>
                <td className="num">{r.load == null ? "-" : r.load.toFixed(2)}</td>
                <td className="num">{r.netIn == null ? "-" : formatRate(r.netIn)}</td>
                <td className="num">{r.netOut == null ? "-" : formatRate(r.netOut)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
