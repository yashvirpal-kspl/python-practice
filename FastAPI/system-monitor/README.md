# VPS Monitor

A FastAPI app that monitors servers with live metrics, history, email alerts, file watching and per-user API keys. It can run as a public service: every user signs up, gets their own key, and only sees their own data.

## Features

- **Live metrics** (psutil): host/uptime, CPU, memory/swap, disks, network, top processes
- **Health check** with configurable warning/critical thresholds
- **History** stored in SQLite, pruned after `RETENTION_DAYS`
- **Email alerts** via SMTP, sent to each server's owner
- **Multi-user:** email sign-up with verification, personal API keys, isolated data
- **Multi-server:** one instance polls other instances running this same app
- **File watching** (watchdog) on the host, with optional email on change
- **Safe for public use:** SSRF guard, hashed keys, rate limits, per-user limits

## Project structure

```
system-monitor/
├── main.py                  # app, lifespan (starts collector + file observer)
├── config.py                # settings loaded from .env
├── db.py                    # SQLite schema + connection helper
├── security.py              # X-API-Key auth: admin key + hashed user keys
├── netguard.py              # blocks private/internal URLs (SSRF guard)
├── models/monitor.py        # Pydantic response/request models
├── routes/
│   ├── system_routes.py     # /system/* (admin only)
│   ├── user_routes.py       # /users/register, /users/verify, /me
│   ├── history_routes.py    # /history, /alerts
│   ├── server_routes.py     # /servers
│   └── observers.py         # /files/events (admin only)
├── services/
│   ├── system_service.py    # psutil metrics + threshold evaluation
│   ├── user_service.py      # registration, email verification, key rotation
│   ├── history_service.py   # store/query samples, pruning
│   ├── alert_service.py     # alert state, cooldown, SMTP email
│   ├── collector.py         # background sampler + remote polling
│   └── observer.py          # watchdog file watcher
├── .env.example
└── requirements.txt
```

## Setup

```bash
python -m venv venv
venv\Scripts\activate          # Linux: source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env           # then edit .env
uvicorn main:app --host 0.0.0.0 --port 8000 --proxy-headers
```

Docs UI: `http://localhost:8000/docs`

Then verify email works: `POST /alerts/test` with your admin key.

## Configuration (`.env`)

| Variable | Default | Description |
|---|---|---|
| `NODE_NAME` | hostname | Name used for this host in history and alerts |
| `API_KEY` | empty | **Admin key.** Full access, including this host's own metrics. Empty = no admin access. Generate with `python -c "import secrets; print(secrets.token_urlsafe(32))"` |
| `DB_PATH` | `monitor.db` | SQLite file |
| `SAMPLE_INTERVAL` | `60` | Seconds between samples |
| `RETENTION_DAYS` | `7` | How long history/alerts/file events are kept |
| `SMTP_HOST`, `SMTP_PORT` | -, `587` | Mail server |
| `SMTP_SSL` | `false` | `true` = implicit SSL (port 465); `false` = STARTTLS (587) |
| `SMTP_USER`, `SMTP_PASSWORD`, `SMTP_FROM` | - | Credentials. For Gmail use an **App Password** |
| `ALERT_TO` | - | Comma-separated recipients for the **host's own** alerts |
| `ALERT_COOLDOWN` | `1800` | Seconds before an unchanged active alert is re-sent |
| `ALLOW_REGISTRATION` | `true` | Allow public sign-up |
| `MAX_SERVERS_PER_USER` | `5` | Servers one user may monitor |
| `VERIFY_TTL_MINUTES` | `30` | Lifetime of an email verification code |
| `REGISTER_PER_IP_PER_HOUR` | `5` | Sign-up attempts per IP |
| `ALLOW_PRIVATE_URLS` | `false` | Let non-admin users add private/loopback server URLs. Dev only, unsafe on a public host |
| `CPU_WARN` / `CPU_CRIT` | `80` / `95` | Percent |
| `MEM_WARN` / `MEM_CRIT` | `80` / `95` | Percent |
| `DISK_WARN` / `DISK_CRIT` | `80` / `90` | Percent, checked per mount point |
| `WATCH_PATHS` | - | Comma-separated directories to watch (recursive) |
| `WATCH_EMAIL` | `false` | Email on file changes (max one per minute) |

## Authentication and users

There are two kinds of keys, both sent in the `X-API-Key` header:

| Key | Who | Can do |
|---|---|---|
| **Admin key** (`API_KEY` in `.env`) | You, the host owner | Everything, including this host's own metrics (`/system/*`, `/files/*`) |
| **User key** | Each registered user | Manage their own servers, view their own history and alerts, receive alerts at their own email |

Only the admin sees the host's metrics. Users cannot see each other's data.

### Getting a user key

1. `POST /users/register {"email": "you@example.com"}` emails a one-time code. The response is the same whether or not the address exists.
2. `POST /users/verify {"email": "you@example.com", "code": "<code>"}` returns the API key. **It is shown once.** Only a hash is stored.

Lost your key? Run the same two steps again. Verifying issues a **new** key and invalidates the old one. `POST /me/rotate-key` also rotates it, and `DELETE /me` removes the account and all of its data.

Registration needs SMTP configured. Emailing a code is how ownership of the address is proven, which also stops the service being used to spam strangers. Set `ALLOW_REGISTRATION=false` to close sign-up.

## API

All endpoints need `X-API-Key` except `/`, `/users/register` and `/users/verify`.

| Method | Path | Who | Description |
|---|---|---|---|
| POST | `/users/register`, `/users/verify` | public | Sign up / get or recover a key |
| GET | `/me` | any | Who the key belongs to |
| POST | `/me/rotate-key` | user | New key, old one stops working |
| DELETE | `/me` | user | Delete account and data |
| GET / POST | `/servers` | any | List / add a server to monitor (own servers only) |
| DELETE | `/servers/{name}` | any | Remove one of your servers |
| GET | `/history?node=&minutes=60&limit=500` | any | Samples, oldest first. Users must pass `node` (see `/history/nodes`); admin defaults to this host |
| GET | `/history/nodes` | any | Your monitored servers with stored history |
| GET | `/alerts?limit=50&node=` | any | Your alert log |
| POST | `/alerts/test` | any | Send a test email to your own address (admin: to `ALERT_TO`) |
| GET | `/system` | admin | Full snapshot of this host |
| GET | `/system/health` | admin | `ok` / `warning` / `critical` plus alert list |
| GET | `/system/host`, `/cpu`, `/memory`, `/disks`, `/network` | admin | Individual sections |
| GET | `/system/processes?limit=10&sort_by=cpu_percent` | admin | Top processes |
| GET | `/files/events?limit=50` | admin | Recent file-change events |

## Email alerts

An email is sent when an alert:

- appears for the first time,
- gets worse (warning to critical), or
- is still active after `ALERT_COOLDOWN`.

A `[RESOLVED]` email is sent when an alert clears. Alerts are keyed per owner, node and metric (`cpu`, `memory`, `disk:<mount>`, `unreachable`), so each is tracked separately. Every alert is also written to the `alerts` table with whether it was emailed.

Alerts for a user's servers go to that user's email. Alerts for the host itself go to `ALERT_TO`.

## Monitoring servers

The monitor **pulls** metrics: it calls `GET /system` on each registered server every `SAMPLE_INTERVAL`, stores the history under that name and emails the owner. So each server you want to monitor runs this same app with its own `API_KEY`. That admin key is what you register as `api_key`:

```bash
curl -X POST https://monitor.example.com/servers \
  -H "X-API-Key: <your user key>" -H "Content-Type: application/json" \
  -d '{"name":"vps-2","url":"https://vps2.example.com","api_key":"<vps-2 admin key>"}'
```

- If a server stops responding, a critical `unreachable` alert is raised. Alert emails are sent from the monitor, so they still arrive when the server is down.
- Server names may only contain letters, digits, `.`, `_` and `-` (they appear in email subjects).

### Protections for a public deployment

- **SSRF guard:** non-admin users cannot register URLs that resolve to private, loopback, link-local or reserved addresses. This is checked when adding **and** again on every poll. Redirects are not followed.
- **Response checks:** remote responses are size-capped and validated against the expected schema.
- **Limits:** `MAX_SERVERS_PER_USER`, a per-IP sign-up rate limit, and at most one verification email per address per minute.
- **Keys:** user keys are random, shown once and stored only as SHA-256 hashes. Verification codes are hashed, expire, and are single-use.

## Notes

- **Windows quirks:** "System Idle Process" can show CPU above 100%. This does not happen on Linux.
- **Root-only data:** `network.connections` is `null` on Linux unless run as root.
- **Blocking samples:** `/system`, `/system/cpu` and `/system/health` block about 1 second while CPU is sampled.
- **HTTPS is required for public use** (for example nginx + Let's Encrypt). API keys travel in a header on every request. Run uvicorn with `--proxy-headers` behind a proxy so the sign-up rate limit sees real client IPs.
- **Secrets:** the keys users give for their remote servers must be sent as-is when polling, so they are stored in plain text in the SQLite file. Anyone who can read the DB file can read them, so protect it. User API keys are hashed.
- **Upgrading from the earlier single-key version:** the database schema changed (user ids were added). Delete the old `monitor.db` so it is recreated.
- **SQLite and scale:** fine for a small public service. For many users, move to PostgreSQL and a proper job queue for polling.
- **Tested (Windows, SMTP mocked):** sign-up and recovery flow, data isolation between users, admin-only host endpoints, SSRF blocking (at add time and at poll time), server limits, alert routing to the owner's email, key rotation and account deletion. Real SMTP delivery and Linux have not been tested.

## Possible next steps

- Run as a `systemd` service on the VPS
- A dashboard UI for the history data
- More alert channels (Telegram, webhook)
- Encrypt stored remote-server keys at rest
- Push-based agent (the server reports in), so users need no open port and the monitor never makes outbound calls to user URLs
