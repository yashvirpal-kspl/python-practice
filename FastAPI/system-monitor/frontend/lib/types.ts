export interface Me {
  id: number;
  email: string | null;
  is_admin: boolean;
}

export interface Sample {
  node: string;
  ts: number; // epoch seconds
  cpu: number | null;
  mem: number | null;
  disk: number | null;
  load1: number | null;
  net_sent_mb: number | null; // cumulative counters
  net_recv_mb: number | null;
}

export interface AlertRecord {
  id: number;
  node: string;
  ts: number;
  level: string; // warning | critical | resolved
  message: string;
  emailed: boolean;
  owner_email?: string | null; // only on admin/alerts
}

export interface Server {
  id: number;
  name: string;
  url: string;
  enabled: boolean;
}

export interface Disk {
  mountpoint: string;
  total_gib: number;
  used_gib: number;
  usage_percent: number;
}

export interface Snapshot {
  host: { hostname: string; platform: string; uptime_seconds: number };
  cpu: { logical_cpus: number | null; usage_percent: number; load_avg: number[] };
  memory: { total_gib: number; used_gib: number; usage_percent: number; swap_percent: number };
  disks: Disk[];
  network: { connections: number | null };
}

export interface Proc {
  pid: number;
  name: string | null;
  username: string | null;
  cpu_percent: number | null;
  memory_percent: number | null;
}

/** One chart row. t is epoch milliseconds. */
export interface Row {
  t: number;
  cpu: number | null;
  mem: number | null;
  disk: number | null;
  load: number | null;
  netIn: number | null; // KB/s
  netOut: number | null; // KB/s
}

export interface OverviewItem {
  user_id: number;
  owner_email: string | null; // null = the admin (this host or the admin's own servers)
  name: string;
  url: string | null;
  enabled: boolean;
  is_host: boolean;
  status: "ok" | "down" | "pending" | "disabled";
  last_seen: number | null;
  cpu: number | null;
  mem: number | null;
  disk: number | null;
  load1: number | null;
}

export interface Overview {
  users: number;
  servers: number;
  items: OverviewItem[];
}
