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
├── backend/                     # FastAPI app (all Python code)
│   ├── main.py                  # app, lifespan (starts collector + file observer)
│   ├── config.py                # settings loaded from ../.env (or backend/.env)
│   ├── db.py                    # SQLite schema + connection helper
│   ├── security.py              # X-API-Key auth: admin key + hashed user keys
│   ├── netguard.py              # blocks private/internal URLs (SSRF guard)
│   ├── models/monitor.py        # Pydantic response/request models
│   ├── routes/
│   │   ├── system_routes.py     # /system/* (admin only)
│   │   ├── user_routes.py       # /users/register, /users/verify, /me
│   │   ├── history_routes.py    # /history, /alerts
│   │   ├── auth_routes.py       # /auth/admin/login, /auth/logout
│   │   ├── admin_routes.py      # /admin/* (overview, users, any server's history)
│   │   ├── server_routes.py     # /servers
│   │   └── observers.py         # /files/events (admin only)
│   ├── services/
│   │   ├── system_service.py    # psutil metrics + threshold evaluation
│   │   ├── user_service.py      # registration, email verification, key rotation
│   │   ├── admin_auth.py        # admin password hashing, sessions, login lockout
│   │   ├── admin_service.py     # admin queries across all users
│   │   ├── history_service.py   # store/query samples, pruning
│   │   ├── alert_service.py     # alert state, cooldown, SMTP email
│   │   ├── collector.py         # background sampler + remote polling
│   │   └── observer.py          # watchdog file watcher
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                    # Next.js dashboard (see "Dashboard" below)
├── docker-compose.yml           # runs backend + frontend
└── .env.example                 # one shared config file for both
```

## Setup

Without Docker, run the backend from the `backend/` folder:

```bash
cp .env.example .env           # in system-monitor/, then edit it
cd backend
python -m venv venv
venv\Scripts\activate          # Linux: source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --proxy-headers
```

The backend reads `../.env` (and `backend/.env` if present, which wins). The SQLite file `monitor.db` is created in `backend/`.

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

Everything is sent in the `X-API-Key` header. There are three kinds of credential:

| Credential | Who | Can do |
|---|---|---|
| **Admin login** (`ADMIN_EMAIL` + `ADMIN_PASSWORD`) | You, signing in to the dashboard | Everything: the host's metrics, plus **every user's servers, history and alerts** |
| **Admin key** (`API_KEY`) | Scripts, and other monitors polling this server | Same access as the admin login, no password needed. Keep it secret |
| **User key** | Each registered user | Manage their own servers, view their own history and alerts, receive alerts at their own email |

Only the admin sees the host's metrics and other users' data. Users cannot see each other's data.

### Admin login (email + password)

Set `ADMIN_EMAIL` and `ADMIN_PASSWORD` in `.env` (password at least 12 characters), restart, then use the **Admin** tab on the dashboard login page. Or call the API:

```bash
curl -X POST http://localhost:8000/auth/admin/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"your password"}'
# -> {"token":"vpsm_s_...","expires_in":43200}   send the token as X-API-Key
```

- The password is stored only as a salted scrypt hash. Session tokens are random, stored only as hashes, last `ADMIN_SESSION_HOURS` (12 by default), and `POST /auth/logout` ends one immediately.
- Changing `ADMIN_EMAIL` or `ADMIN_PASSWORD` and restarting replaces the account and signs out every session. If either is empty or the password is too short, password login is disabled (the app logs why).
- Wrong email and wrong password give the same error. After `LOGIN_MAX_FAILURES` (5) failures from one IP, that IP is locked out for `LOGIN_LOCK_MINUTES` (15). This limit is in memory and resets on restart.
- **Use HTTPS in production.** The password and the session token cross the network on every login and request.

### Getting a user key

1. `POST /users/register {"email": "you@example.com"}` emails a one-time code. The response is the same whether or not the address exists.
2. `POST /users/verify {"email": "you@example.com", "code": "<code>"}` returns the API key. **It is shown once.** Only a hash is stored.

Lost your key? Run the same two steps again. Verifying issues a **new** key and invalidates the old one. `POST /me/rotate-key` also rotates it, and `DELETE /me` removes the account and all of its data.

Registration needs SMTP configured. Emailing a code is how ownership of the address is proven, which also stops the service being used to spam strangers. Set `ALLOW_REGISTRATION=false` to close sign-up.

## API

All endpoints need `X-API-Key` except `/`, `/users/register`, `/users/verify` and `/auth/admin/login`.

| Method | Path | Who | Description |
|---|---|---|---|
| POST | `/users/register`, `/users/verify` | public | Sign up / get or recover a key |
| POST | `/auth/admin/login` | public | Admin email + password, returns a session token |
| POST | `/auth/logout` | any | End an admin session |
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
| GET | `/admin/overview` | admin | Every server (this host first) with owner, status (`ok` / `down` / `pending` / `disabled`) and latest CPU, memory, disk, load |
| GET | `/admin/users` | admin | All users with server counts |
| GET | `/admin/history?user_id=&node=&minutes=&limit=` | admin | History of any user's server (`user_id=0` is the host) |
| GET | `/admin/alerts?limit=50` | admin | Alerts across all users, with the owner's email |

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

## Dashboard (Next.js)

The web UI lives in [frontend/](frontend/). It talks to this API through its own server routes, so the browser never sees an API key.

```bash
cd frontend
cp .env.local.example .env.local     # BACKEND_URL=http://127.0.0.1:8000
npm install
npm run dev                          # http://localhost:3000
```

Start the backend first (`uvicorn main:app --port 8000`). For production use `npm run build && npm start`.

**What it shows**
- Sign-in with an API key, sign-up / key recovery with the email code flow (the new key is shown once), or **admin sign-in with email and password**
- Server picker and time range (15 min to 7 days), with optional 30-second auto-refresh
- Latest values, then charts for CPU, memory, disk, load and network throughput (hover for exact values), or a table view of the same samples
- Alerts list with a "send test email" button, and add/remove servers
- **Admin only:** an "All servers" table across every user (owner, up/down status, latest CPU, memory and disk, last seen) with a "View charts" button for any server, a live panel for the host itself (disks, memory, top processes), and alerts from all users

**How it works**
- `app/api/auth/*` checks the key against the backend and stores it in an `httpOnly`, `SameSite=Lax` cookie. Page JavaScript cannot read it.
- `app/api/backend/[...path]` is a proxy that adds the cookie's key as `X-API-Key`. It only forwards `me`, `servers`, `history`, `alerts`, `system` and `files`.
- No CORS setup is needed because the browser only talks to the Next.js server.
- Network charts show KB/s, calculated from the stored cumulative counters. Long ranges are averaged down to at most 240 points.

**Deploying**
- Serve the dashboard over HTTPS. The session cookie is `Secure` in production builds (override with `COOKIE_SECURE`).
- Keep the backend off the public internet if only the dashboard needs it, or put both behind one reverse proxy.
- The sign-up limit counts per IP. The dashboard forwards the visitor's `X-Forwarded-For`, and uvicorn only trusts it from its `--forwarded-allow-ips` (default `127.0.0.1`), so run both on one host or set that option to the dashboard's address.
- `GET /history` returns at most 5000 samples. At the default 60 s interval that covers about 3.5 days, so the 7-day view shows the most recent 3.5 days until the limit is raised in [backend/routes/history_routes.py](backend/routes/history_routes.py) or `SAMPLE_INTERVAL` is increased.

## Docker

`docker-compose.yml` runs the API and the dashboard together.

```bash
cp .env.example .env        # set API_KEY, SMTP_*, ALERT_TO
docker compose up -d --build
```

Dashboard: `http://localhost:3000` (sign in with your `API_KEY` as admin). The API is published on `127.0.0.1:8000` only.

| Setting (shell or `.env`) | Default | Purpose |
|---|---|---|
| `BACKEND_BIND` | `127.0.0.1` | Address the API port binds to. Use `0.0.0.0` if other monitors must poll this server |
| `FRONTEND_BIND` | `0.0.0.0` | Address the dashboard binds to |
| `DISK_PATHS` | `/=/host` | Disks to report as `label=path`. See below |
| `COOKIE_SECURE` | auto | Set `false` only for plain-http access on a non-localhost address |
| `FORWARDED_ALLOW_IPS` | `*` | Who uvicorn trusts for `X-Forwarded-For`. Set to your proxy's address if the API is public |

**What the container can see**
- **CPU, memory and load** come from the kernel, so they are the host's.
- **Disks:** the host's `/` is mounted read-only at `/host` and `DISK_PATHS=/=/host` reports it as `/`. Add more with e.g. `DISK_PATHS=/=/host,/data=/host/mnt/data`. Without this the container would only report its own filesystem. The mount is read-only, but it does expose the host's files to the app, so keep the API key private.
- **Processes:** by default only the container's. Uncomment `pid: host` in the compose file to list the host's.
- **Network:** counters are the container's own interface. For the host's total traffic, use `network_mode: host` on the backend and point `BACKEND_URL` at the host.
- **File watching:** mount the directory and list it, e.g. `WATCH_PATHS=/host/var/www`.
- **Data:** the SQLite file lives in the `monitor-data` volume and survives rebuilds. Back up with `docker run --rm -v system-monitor_monitor-data:/d -v "$PWD":/b alpine tar czf /b/monitor-data.tgz -C /d .`.
- **Per-IP sign-up limit:** put a reverse proxy in front of the dashboard that sets `X-Forwarded-For`. Otherwise every visitor looks like the same address.

**Building behind a corporate proxy:** if `npm install` fails with `UNABLE_TO_VERIFY_LEAF_SIGNATURE`, your network re-signs HTTPS traffic. Export your organisation's root CA as PEM, save it as `frontend/certs/corp.crt`, and rebuild. Do not turn off TLS verification.

**Dependencies are not locked.** `frontend/package-lock.json` does not exist yet, so builds install the newest versions allowed by `package.json`. Generate one with `npm install` in `frontend/` and commit it.

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
