import asyncio
import json
import os
import hashlib
import secrets
import time
import aiofiles
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from urllib.parse import quote
from collections import deque, defaultdict
from pathlib import Path

from fastapi import FastAPI, Request, HTTPException, Depends, WebSocket
from fastapi.responses import Response, HTMLResponse, JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import httpx
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("Kourosh")

IRAN_TZ = ZoneInfo("Asia/Tehran")

app = FastAPI(title="Kourosh", docs_url=None, redoc_url=None)

# ── Persistence ───────────────────────────────────────────────────────────────
def resolve_data_dir() -> Path:
    env_dir = os.environ.get("DATA_DIR") or os.environ.get("RAILWAY_VOLUME_MOUNT_PATH")
    if env_dir:
        return Path(env_dir)
    if Path("/data").exists() and os.access("/data", os.W_OK):
        return Path("/data")
    return Path("./data")

DATA_DIR = resolve_data_dir()
DATA_FILE = DATA_DIR / "x4g_state.json"
SECRET_FILE = DATA_DIR / "x4g_secret.key"
SAVE_LOCK = asyncio.Lock()

def _load_or_create_secret() -> str:
    env_secret = os.environ.get("SECRET_KEY")
    if env_secret:
        return env_secret
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        if SECRET_FILE.exists():
            existing = SECRET_FILE.read_text(encoding="utf-8").strip()
            if existing:
                return existing
        new_secret = secrets.token_urlsafe(32)
        SECRET_FILE.write_text(new_secret, encoding="utf-8")
        return new_secret
    except Exception as e:
        logger.warning(f"Could not persist SECRET_KEY: {e}")
        return secrets.token_urlsafe(32)

CONFIG = {
    "port": int(os.environ.get("PORT", 8080)),
    "secret": _load_or_create_secret(),
    "host": os.environ.get("RAILWAY_PUBLIC_DOMAIN", "localhost"),
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SETTINGS = {
    "worker_domain": os.environ.get("WORKER_DOMAIN", "").strip(),
    "clean_ip": os.environ.get("CLEAN_IP", "").strip(),
}

async def load_state():
    global LINKS, AUTH, SUBS, SETTINGS
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        if DATA_FILE.exists():
            async with aiofiles.open(DATA_FILE, "r", encoding="utf-8") as f:
                raw = await f.read()
            data = json.loads(raw)
            LINKS.update(data.get("links", {}))
            SUBS.update(data.get("subs", {}))
            SETTINGS.update(data.get("settings", {}))
            if "password_hash" in data:
                AUTH["password_hash"] = data["password_hash"]
            legacy_default_uids = [uid for uid, l in LINKS.items() if l.get("is_default")]
            for uid in legacy_default_uids:
                LINKS.pop(uid, None)
            if legacy_default_uids:
                asyncio.create_task(save_state())
            logger.info(f"State loaded: {len(LINKS)} links, {len(SUBS)} subs, worker_domain='{SETTINGS.get('worker_domain')}'")
    except Exception as e:
        logger.warning(f"Could not load state: {e}")

async def save_state():
    async with SAVE_LOCK:
        try:
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            data = {
                "links": dict(LINKS),
                "subs": dict(SUBS),
                "settings": dict(SETTINGS),
                "password_hash": AUTH["password_hash"],
                "saved_at": datetime.now().isoformat(),
            }
            tmp = DATA_FILE.with_suffix(".tmp")
            async with aiofiles.open(tmp, "w", encoding="utf-8") as f:
                await f.write(json.dumps(data, ensure_ascii=False, indent=2))
            tmp.replace(DATA_FILE)
        except Exception as e:
            logger.warning(f"Could not save state: {e}")

# ── In-memory state ───────────────────────────────────────────────────────────
connections: dict = {}
stats = {
    "total_bytes": 0,
    "total_requests": 0,
    "total_errors": 0,
    "start_time": time.time(),
}
error_logs: deque = deque(maxlen=50)
activity_logs: deque = deque(maxlen=200)
hourly_traffic: dict = defaultdict(int)
http_client: httpx.AsyncClient | None = None
LINKS: dict = {}
LINKS_LOCK = asyncio.Lock()
SUBS: dict = {}
SUBS_LOCK = asyncio.Lock()

# Protocol and configuration standards
PROTOCOLS = ("vless-grpc", "vless-ws", "xhttp", "custom")
DEFAULT_PROTOCOL = "vless-grpc"

FINGERPRINTS = ("chrome", "firefox", "safari", "ios", "android", "edge", "360", "qq", "random", "randomized")
DEFAULT_FINGERPRINT = "chrome"

DEFAULT_PORT = 443
ALLOWED_PORTS = (443, 8443)

DEFAULT_SPEED_LIMIT = 0

def log_activity(kind: str, message: str, level: str = "info"):
    activity_logs.append({
        "kind": kind,
        "level": level,
        "message": message,
        "time": datetime.now().isoformat(),
    })

# ── Auth ──────────────────────────────────────────────────────────────────────
SESSION_COOKIE = "x4g_session"
SESSION_TTL = 60 * 60 * 24 * 365

def hash_password(pw: str) -> str:
    return hashlib.sha256(f"{pw}{CONFIG['secret']}".encode()).hexdigest()

AUTH = {"password_hash": hash_password(os.environ.get("ADMIN_PASSWORD", "KouroshKING"))}
SESSIONS: dict = {}
SESSIONS_LOCK = asyncio.Lock()

async def create_session() -> str:
    token = secrets.token_urlsafe(32)
    async with SESSIONS_LOCK:
        SESSIONS[token] = time.time() + SESSION_TTL
    return token

async def is_valid_session(token: str | None) -> bool:
    if not token:
        return False
    async with SESSIONS_LOCK:
        exp = SESSIONS.get(token)
        if exp is None:
            return False
        if exp < time.time():
            SESSIONS.pop(token, None)
            return False
        return True

async def destroy_session(token: str | None):
    if not token:
        return
    async with SESSIONS_LOCK:
        SESSIONS.pop(token, None)

async def require_auth(request: Request):
    token = request.cookies.get(SESSION_COOKIE)
    if not await is_valid_session(token):
        raise HTTPException(status_code=401, detail="unauthorized")
    return token

# ── Startup / Shutdown ────────────────────────────────────────────────────────
@app.on_event("startup")
async def startup():
    global http_client
    limits = httpx.Limits(max_connections=500, max_keepalive_connections=100)
    timeout = httpx.Timeout(30.0, connect=10.0)
    http_client = httpx.AsyncClient(
        limits=limits, timeout=timeout, follow_redirects=True,
    )
    await load_state()
    log_activity("system", "سرور راه‌اندازی شد", "ok")
    logger.info(f"Kourosh Panel v9.8 started on port {CONFIG['port']}")

@app.on_event("shutdown")
async def shutdown():
    await save_state()
    if http_client:
        await http_client.aclose()

# ── Helpers ───────────────────────────────────────────────────────────────────
def get_host(request: Request | None = None) -> str:
    if request is not None:
        h = request.headers.get("x-forwarded-host") or request.headers.get("host")
        if h:
            h = h.split(":")[0]
            CONFIG["host"] = h
            return h
    return os.environ.get("RAILWAY_PUBLIC_DOMAIN", CONFIG["host"])

def generate_uuid() -> str:
    h = secrets.token_hex(16)
    return f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:32]}"
    
def now_ir() -> datetime:
    return datetime.now(IRAN_TZ)

def generate_vless_link(
    uuid: str,
    host: str,
    remark: str = "Kourosh",
    protocol: str = DEFAULT_PROTOCOL,
    fingerprint: str | None = None,
    alpn: str | None = None,
    port: int | None = None,
    worker_domain: str | None = None,
    clean_ip: str | None = None,
    sni: str | None = None,
    host_header: str | None = None,
    fragment_packets: str | None = None,
    fragment_length: str | None = None,
    fragment_interval: str | None = None,
    mux_enable: bool = False,
    mux_concurrency: int = 8,
) -> str:
    """ساخت لینک‌های VLESS استاندارد و پیشرفته مطابق دقیق با تنظیمات انتخابی پنل"""
    port_val = port or DEFAULT_PORT
    if port_val not in ALLOWED_PORTS:
        port_val = DEFAULT_PORT

    service_name = secrets.token_urlsafe(6)
    proto = (protocol or DEFAULT_PROTOCOL).lower()
    
    # Global / Worker settings
    w_domain = (worker_domain or SETTINGS.get("worker_domain") or "").strip()
    c_ip = (clean_ip or SETTINGS.get("clean_ip") or "").strip()

    # Address resolution: Config clean_ip -> Global clean_ip -> Worker Domain -> Host
    if c_ip:
        target_addr = c_ip
    elif w_domain:
        target_addr = w_domain
    else:
        target_addr = host

    # SNI resolution: Config sni -> Worker Domain -> Host
    if sni and sni.strip():
        target_sni = sni.strip()
    elif w_domain:
        target_sni = w_domain
    else:
        target_sni = host

    # Host Header resolution: Config host_header -> Worker Domain -> Host
    if host_header and host_header.strip():
        target_host = host_header.strip()
    elif w_domain:
        target_host = w_domain
    else:
        target_host = host

    # Fingerprint resolution
    target_fp = (fingerprint or DEFAULT_FINGERPRINT).strip().lower()

    # ALPN resolution: default http/1.1 for ws/xhttp, h2 for grpc
    if alpn and alpn.strip():
        target_alpn = alpn.strip()
    else:
        target_alpn = "h2" if proto == "vless-grpc" else "http/1.1"

    # Transport type
    if proto == "vless-ws":
        type_str = "ws"
    elif proto == "xhttp":
        type_str = "xhttp"
    else:
        type_str = "grpc"

    # Standard required parameters in exact order matching user specification
    params = [
        ("encryption", "none"),
        ("security", "tls"),
        ("sni", target_sni),
        ("fp", target_fp),
        ("alpn", target_alpn),
        ("insecure", "0"),
        ("allowInsecure", "0"),
        ("type", type_str),
        ("host", target_host),
    ]

    # Path / ServiceName / Mode according to transport protocol
    if proto == "vless-ws":
        params.append(("path", f"/ws/{uuid}"))
    elif proto == "xhttp":
        params.append(("path", f"/xhttp-siz10/{uuid}"))
        params.append(("mode", "auto"))
    else:
        params.append(("serviceName", service_name))

    # Optional Fragment parameters (ONLY if fragment_packets is explicitly filled)
    fg_p = (fragment_packets or "").strip()
    if fg_p:
        params.append(("fragment", fg_p))
        params.append(("fg-len", (fragment_length or "10-20").strip()))
        params.append(("fg-interval", (fragment_interval or "10-20").strip()))

    # Optional Mux parameters (ONLY if mux_enable is True)
    if mux_enable:
        params.append(("mux", "1"))
        params.append(("mux-concurrency", str(mux_concurrency if mux_concurrency > 0 else 8)))

    query = "&".join(f"{k}={quote(str(v), safe='')}" for k, v in params)
    return f"vless://{uuid}@{target_addr}:{port_val}?{query}#{quote(remark)}"

def vless_link_for_link(link: dict, uid: str, host: str) -> str:
    proto = link.get("protocol", DEFAULT_PROTOCOL)
    if proto == "custom":
        raw = (link.get("custom_uri") or "").strip()
        if not raw:
            return f"socks://{uid}@{host}:1080#{quote('Kourosh-' + link.get('label',''))}"
        return raw.replace("{host}", host).replace("{uuid}", uid)
    return generate_vless_link(
        uuid=uid,
        host=host,
        remark=f"Kourosh-{link.get('label','')}",
        protocol=proto,
        fingerprint=link.get("fingerprint"),
        alpn=link.get("alpn"),
        port=link.get("port"),
        worker_domain=link.get("worker_domain"),
        clean_ip=link.get("clean_ip"),
        sni=link.get("sni"),
        host_header=link.get("host"),
        fragment_packets=link.get("fragment_packets"),
        fragment_length=link.get("fragment_length"),
        fragment_interval=link.get("fragment_interval"),
        mux_enable=bool(link.get("mux_enable", False)),
        mux_concurrency=int(link.get("mux_concurrency", 8) or 8),
    )

def uptime() -> str:
    secs = int(time.time() - stats["start_time"])
    h, m, s = secs // 3600, (secs % 3600) // 60, secs % 60
    return f"{h:02d}:{m:02d}:{s:02d}"

async def check_and_use(uid: str, n: int) -> bool:
    async with LINKS_LOCK:
        link = LINKS.get(uid)
        if link is None:
            return False
        if not is_link_allowed(link):
            return False
        link["used_bytes"] += n
        
        sub_id = link.get("sub_id")
        if sub_id:
            sub = SUBS.get(sub_id)
            if sub:
                sub["used_bytes"] += n

        stats["total_bytes"] += n
        hourly_traffic[now_ir().strftime("%H:00")] += n
    return True

def parse_size_to_bytes(value: float, unit: str) -> int:
    unit = unit.upper()
    if unit == "GB": return int(value * 1024 ** 3)
    if unit == "MB": return int(value * 1024 ** 2)
    if unit == "KB": return int(value * 1024)
    return int(value)

def parse_speed_to_bytes(value: float, unit: str) -> int:
    if value <= 0:
        return 0
    unit = (unit or "MBIT").upper()
    if unit == "MBIT":
        return int(value * 1024 * 1024 / 8)
    if unit == "KB":
        return int(value * 1024)
    if unit == "MB":
        return int(value * 1024 * 1024)
    return int(value)

def is_link_expired(link: dict) -> bool:
    exp = link.get("expires_at")
    if not exp:
        return False
    try:
        return datetime.now() > datetime.fromisoformat(exp)
    except Exception:
        return False

def is_sub_expired(sub: dict) -> bool:
    exp = sub.get("expires_at")
    if not exp:
        return False
    try:
        return datetime.now() > datetime.fromisoformat(exp)
    except Exception:
        return False

def is_link_allowed(link: dict | None) -> bool:
    if link is None:
        return False
    if not link.get("active", True):
        return False
    if is_link_expired(link):
        return False
    lb = link.get("limit_bytes", 0)
    if lb > 0 and link.get("used_bytes", 0) >= lb:
        return False
        
    sub_id = link.get("sub_id")
    if sub_id and sub_id in SUBS:
        sub = SUBS[sub_id]
        if not sub.get("active", True):
            return False
        if is_sub_expired(sub):
            return False
        slb = sub.get("limit_bytes", 0)
        if slb > 0 and sub.get("used_bytes", 0) >= slb:
            return False
            
    return True

def fmt_bytes(b: int) -> str:
    if b < 1024: return f"{b} B"
    if b < 1024**2: return f"{b/1024:.1f} KB"
    if b < 1024**3: return f"{b/1024**2:.2f} MB"
    return f"{b/1024**3:.2f} GB"

def unique_ips_for_uuid(uuid: str) -> set:
    return {c.get("ip") for c in list(connections.values()) if c.get("uuid") == uuid and c.get("ip")}

def unique_ips_for_sub(sub_id: str) -> set:
    sub_links = {uid for uid, l in LINKS.items() if l.get("sub_id") == sub_id}
    return {c.get("ip") for c in list(connections.values()) if c.get("uuid") in sub_links and c.get("ip")}

def is_ip_allowed(link: dict | None, uuid: str, ip: str) -> bool:
    if link is None:
        return False
        
    sub_id = link.get("sub_id")
    if sub_id and sub_id in SUBS:
        sub_limit = int(SUBS[sub_id].get("ip_limit", 0) or 0)
        if sub_limit > 0:
            ips = unique_ips_for_sub(sub_id)
            if ip not in ips and len(ips) >= sub_limit:
                return False
                
    limit = int(link.get("ip_limit", 0) or 0)
    if limit > 0:
        ips = unique_ips_for_uuid(uuid)
        if ip not in ips and len(ips) >= limit:
            return False
            
    return True

def client_ip(request: Request) -> str:
    fwd = request.headers.get("x-forwarded-for")
    if fwd:
        return fwd.split(",")[0].strip()
    real_ip = request.headers.get("x-real-ip")
    if real_ip:
        return real_ip.strip()
    return request.client.host if request.client else "نامشخص"

# ── Basic endpoints ───────────────────────────────────────────────────────────
@app.get("/")
async def root():
    return {"service": "Kourosh", "version": "9.8", "status": "active", "channel": "https://t.me/kouroxlog"}

@app.get("/health")
async def health():
    return {"status": "ok", "connections": len(connections), "uptime": uptime()}

# ── Subscription (Public Feed for V2ray / Sing-Box / Xray Clients) ───────────
@app.get("/sub/{uuid}")
async def subscription_single(uuid: str, request: Request):
    import base64
    host = get_host(request)
    
    # Check if it's a Subscription ID
    async with SUBS_LOCK:
        sub = SUBS.get(uuid)
        
    if sub:
        if not sub.get("active", True) or is_sub_expired(sub):
            raise HTTPException(status_code=404, detail="subscription inactive or expired")
            
        async with LINKS_LOCK:
            sub_links = [
                vless_link_for_link(l, uid, host) 
                for uid, l in LINKS.items() 
                if l.get("sub_id") == uuid and is_link_allowed(l)
            ]
            
        content = base64.b64encode("\n".join(sub_links).encode()).decode()
        
        headers = {
            "profile-title": quote(sub.get("label", "Kourosh Sub")),
            "support-url": "https://t.me/kouroxlog"
        }
        
        upload = 0
        download = sub.get("used_bytes", 0)
        total = sub.get("limit_bytes", 0)
        
        expire_str = ""
        if sub.get("expires_at"):
            try:
                dt = datetime.fromisoformat(sub["expires_at"])
                expire_str = f"; expire={int(dt.timestamp())}"
            except: pass
            
        if total > 0 or expire_str:
            headers["subscription-userinfo"] = f"upload={upload}; download={download}; total={total}{expire_str}"
            
        return Response(content=content, media_type="text/plain", headers=headers)
        
    # Check if it's a single config UUID
    async with LINKS_LOCK:
        link = LINKS.get(uuid)
    if not link or not is_link_allowed(link):
        raise HTTPException(status_code=404, detail="not found or inactive")
        
    vless = vless_link_for_link(link, uuid, host)
    content = base64.b64encode(vless.encode()).decode()
    return Response(content=content, media_type="text/plain",
                    headers={"profile-title": quote(link["label"]), "support-url": "https://t.me/kouroxlog"})

@app.get("/sub-all")
async def subscription_all(request: Request, _=Depends(require_auth)):
    import base64
    host = get_host(request)
    async with LINKS_LOCK:
        lines = [
            vless_link_for_link(d, uid, host)
            for uid, d in LINKS.items()
            if is_link_allowed(d)
        ]
    content = base64.b64encode("\n".join(lines).encode()).decode()
    return Response(content=content, media_type="text/plain")

# ── Auth endpoints ────────────────────────────────────────────────────────────
@app.post("/api/login")
async def api_login(request: Request):
    body = await request.json()
    ip = client_ip(request)
    if hash_password(str(body.get("password", ""))) != AUTH["password_hash"]:
        log_activity("auth", f"تلاش ورود ناموفق از {ip}", "err")
        raise HTTPException(status_code=401, detail="رمز عبور اشتباه است")
    token = await create_session()
    log_activity("auth", f"ورود موفق به پنل از {ip}", "ok")
    resp = JSONResponse({"ok": True})
    resp.set_cookie(SESSION_COOKIE, token, max_age=SESSION_TTL, httponly=True, samesite="lax", path="/")
    return resp

@app.post("/api/logout")
async def api_logout(request: Request):
    await destroy_session(request.cookies.get(SESSION_COOKIE))
    resp = JSONResponse({"ok": True})
    resp.delete_cookie(SESSION_COOKIE, path="/")
    return resp

@app.get("/api/me")
async def api_me(request: Request):
    return {"authenticated": await is_valid_session(request.cookies.get(SESSION_COOKIE))}

@app.post("/api/change-password")
async def api_change_password(request: Request, token=Depends(require_auth)):
    body = await request.json()
    if hash_password(str(body.get("current_password", ""))) != AUTH["password_hash"]:
        raise HTTPException(status_code=400, detail="رمز فعلی اشتباه است")
    new = str(body.get("new_password", ""))
    if len(new) < 4:
        raise HTTPException(status_code=400, detail="رمز جدید باید حداقل ۴ کاراکتر باشد")
    AUTH["password_hash"] = hash_password(new)
    async with SESSIONS_LOCK:
        SESSIONS.clear()
        SESSIONS[token] = time.time() + SESSION_TTL
    await save_state()
    log_activity("auth", "رمز عبور پنل تغییر کرد", "ok")
    return {"ok": True}

# ── Settings API (Cloudflare Worker & Clean IP) ──────────────────────────────
@app.get("/api/settings")
async def get_settings(_=Depends(require_auth)):
    return {
        "worker_domain": SETTINGS.get("worker_domain", ""),
        "clean_ip": SETTINGS.get("clean_ip", ""),
    }

@app.post("/api/settings")
async def update_settings(request: Request, _=Depends(require_auth)):
    body = await request.json()
    if "worker_domain" in body:
        SETTINGS["worker_domain"] = str(body["worker_domain"]).strip()
    if "clean_ip" in body:
        SETTINGS["clean_ip"] = str(body["clean_ip"]).strip()
    await save_state()
    log_activity("settings", "تنظیمات وورکر کلادفلر بروزرسانی شد", "ok")
    return {"ok": True, "settings": dict(SETTINGS)}

# ── Stats ─────────────────────────────────────────────────────────────────────
@app.get("/stats")
async def get_stats(_=Depends(require_auth)):
    async with LINKS_LOCK:
        snap_links = dict(LINKS)
    async with SUBS_LOCK:
        snap_subs = dict(SUBS)
    return {
        "active_connections": len(connections),
        "total_traffic_mb": round(stats["total_bytes"] / (1024 ** 2), 2),
        "total_requests": stats["total_requests"],
        "total_errors": stats["total_errors"],
        "uptime": uptime(),
        "timestamp": datetime.now().isoformat(),
        "hourly": dict(hourly_traffic),
        "recent_errors": list(error_logs)[-10:],
        "links_count": len(snap_links),
        "active_links": sum(1 for l in snap_links.values() if is_link_allowed(l)),
        "expired_links": sum(1 for l in snap_links.values() if is_link_expired(l)),
        "subs_count": len(snap_subs),
        "active_subs": sum(1 for s in snap_subs.values() if s.get("active", True) and not is_sub_expired(s)),
        "proto_dist": {
            "vless_ws": sum(1 for l in snap_links.values() if l.get("protocol") == "vless-ws"),
            "vless_grpc": sum(1 for l in snap_links.values() if l.get("protocol") == "vless-grpc" or not l.get("protocol")),
            "xhttp": sum(1 for l in snap_links.values() if l.get("protocol") == "xhttp"),
            "custom": sum(1 for l in snap_links.values() if l.get("protocol") == "custom"),
        }
    }

# ── Activity Logs ─────────────────────────────────────────────────────────────
@app.get("/api/activity")
async def get_activity(_=Depends(require_auth)):
    return {"logs": list(activity_logs)[-150:]}

# ── Live connections ──────────────────────────────────────────────────────────
@app.get("/api/connections")
async def get_connections(_=Depends(require_auth)):
    async with LINKS_LOCK:
        snap = dict(LINKS)

    by_uuid: dict[str, dict] = {}
    for conn_id, c in connections.items():
        uid = c.get("uuid", "نامشخص")
        ip = c.get("ip", "نامشخص")
        link = snap.get(uid)
        label = link.get("label") if link else "کانفیگ حذف‌شده"
        proto = link.get("protocol", DEFAULT_PROTOCOL) if link else "?"

        cfg = by_uuid.get(uid)
        if cfg is None:
            cfg = {
                "uuid": uid,
                "label": label,
                "protocol": proto,
                "sessions": 0,
                "bytes": 0,
                "ips": {},
                "first_connected_at": c.get("connected_at"),
                "last_connected_at": c.get("connected_at"),
            }
            by_uuid[uid] = cfg
        cfg["sessions"] += 1
        cfg["bytes"] += c.get("bytes", 0)

        ip_entry = cfg["ips"].get(ip)
        if ip_entry is None:
            ip_entry = {
                "ip": ip, "sessions": 0, "bytes": 0, "transports": set(),
                "first_connected_at": c.get("connected_at"),
                "last_connected_at": c.get("connected_at"),
            }
            cfg["ips"][ip] = ip_entry
        ip_entry["sessions"] += 1
        ip_entry["bytes"] += c.get("bytes", 0)
        ip_entry["transports"].add(c.get("transport", "vless-grpc"))

        ca = c.get("connected_at")
        for entry in (cfg, ip_entry):
            if ca:
                if not entry["first_connected_at"] or ca < entry["first_connected_at"]:
                    entry["first_connected_at"] = ca
                if not entry["last_connected_at"] or ca > entry["last_connected_at"]:
                    entry["last_connected_at"] = ca

    configs = []
    for uid, cfg in by_uuid.items():
        ip_list = []
        for ip, e in cfg["ips"].items():
            ip_list.append({
                "ip": ip,
                "sessions": e["sessions"],
                "bytes": e["bytes"],
                "bytes_fmt": fmt_bytes(e["bytes"]),
                "transports": sorted(e["transports"]),
                "connected_at": e["first_connected_at"],
                "last_connected_at": e["last_connected_at"],
            })
        ip_list.sort(key=lambda x: x.get("last_connected_at") or "", reverse=True)
        configs.append({
            "uuid": uid,
            "label": cfg["label"],
            "protocol": cfg["protocol"],
            "ip_count": len(ip_list),
            "sessions": cfg["sessions"],
            "bytes": cfg["bytes"],
            "bytes_fmt": fmt_bytes(cfg["bytes"]),
            "connected_at": cfg["first_connected_at"],
            "last_connected_at": cfg["last_connected_at"],
            "connections": ip_list,
        })
    configs.sort(key=lambda x: x.get("last_connected_at") or "", reverse=True)

    return {
        "configs": configs,
        "count": len(configs),
        "raw_count": len(connections),
    }

# ── Link Creation Helper ──────────────────────────────────────────────────────
async def make_link(
    label: str = "لینک جدید",
    limit_bytes: int = 0,
    expires_at: str | None = None,
    note: str = "",
    protocol: str = DEFAULT_PROTOCOL,
    fingerprint: str = DEFAULT_FINGERPRINT,
    alpn: str = "",
    port: int = DEFAULT_PORT,
    ip_limit: int = 0,
    speed_limit_bytes: int = 0,
    sub_id: str | None = None,
    clean_ip: str = "",
    sni: str = "",
    host_header: str = "",
    fragment_packets: str = "",
    fragment_length: str = "10-20",
    fragment_interval: str = "10-20",
    mux_enable: bool = False,
    mux_concurrency: int = 8,
    custom_uri: str = "",
) -> tuple[str, dict]:
    if protocol not in PROTOCOLS:
        protocol = DEFAULT_PROTOCOL
    fingerprint = (fingerprint or DEFAULT_FINGERPRINT).strip().lower()
    if fingerprint not in FINGERPRINTS:
        fingerprint = DEFAULT_FINGERPRINT
    if port not in ALLOWED_PORTS:
        port = DEFAULT_PORT
    uid = generate_uuid()
    async with LINKS_LOCK:
        LINKS[uid] = {
            "label": (label or "لینک جدید").strip()[:60] or "لینک جدید",
            "limit_bytes": max(0, limit_bytes),
            "used_bytes": 0,
            "created_at": datetime.now().isoformat(),
            "active": True,
            "expires_at": expires_at,
            "note": (note or "").strip()[:200],
            "is_default": False,
            "protocol": protocol,
            "fingerprint": fingerprint,
            "alpn": (alpn or "").strip()[:100],
            "port": port,
            "ip_limit": max(0, ip_limit),
            "speed_limit_bytes": max(0, speed_limit_bytes),
            "sub_id": sub_id,
            "clean_ip": (clean_ip or "").strip(),
            "sni": (sni or "").strip(),
            "host": (host_header or "").strip(),
            "fragment_packets": (fragment_packets or "").strip(),
            "fragment_length": (fragment_length or "10-20").strip(),
            "fragment_interval": (fragment_interval or "10-20").strip(),
            "mux_enable": bool(mux_enable),
            "mux_concurrency": max(1, int(mux_concurrency or 8)),
            "custom_uri": (custom_uri or "").strip(),
        }
    asyncio.create_task(save_state())
    log_activity("link", f"کانفیگ «{LINKS[uid]['label']}» ساخته شد", "ok")
    return uid, LINKS[uid]

async def remove_link(uid: str) -> str | None:
    async with LINKS_LOCK:
        if uid not in LINKS:
            return None
        label = LINKS[uid].get("label", uid)
        del LINKS[uid]
    asyncio.create_task(save_state())
    log_activity("link", f"کانفیگ «{label}» حذف شد", "err")
    return label

async def set_link_active(uid: str, active: bool) -> dict | None:
    async with LINKS_LOCK:
        if uid not in LINKS:
            return None
        LINKS[uid]["active"] = bool(active)
        label = LINKS[uid]["label"]
    log_activity("link", f"کانفیگ «{label}» {'فعال' if active else 'غیرفعال'} شد", "ok" if active else "warn")
    asyncio.create_task(save_state())
    return LINKS[uid]

# ── Link Management APIs ──────────────────────────────────────────────────────
@app.post("/api/links")
async def create_link(request: Request, _=Depends(require_auth)):
    body = await request.json()
    lv = float(body.get("limit_value") or 0)
    lu = body.get("limit_unit") or "GB"
    limit_bytes = 0 if lv <= 0 else parse_size_to_bytes(lv, lu)
    exp_days = int(body.get("expires_days") or 0)
    expires_at = (datetime.now() + timedelta(days=exp_days)).isoformat() if exp_days > 0 else None
    try:
        port = int(body.get("port") or DEFAULT_PORT)
    except (TypeError, ValueError):
        port = DEFAULT_PORT
    try:
        ip_limit = int(body.get("ip_limit") or 0)
    except (TypeError, ValueError):
        ip_limit = 0

    sv = float(body.get("speed_limit_value") or 0)
    su = body.get("speed_limit_unit") or "MBIT"
    speed_limit_bytes = 0 if sv <= 0 else parse_speed_to_bytes(sv, su)

    uid, link = await make_link(
        label=body.get("label") or "لینک جدید",
        limit_bytes=limit_bytes,
        expires_at=expires_at,
        note=body.get("note") or "",
        protocol=body.get("protocol") or DEFAULT_PROTOCOL,
        fingerprint=body.get("fingerprint") or DEFAULT_FINGERPRINT,
        alpn=body.get("alpn") or "",
        port=port,
        ip_limit=ip_limit,
        speed_limit_bytes=speed_limit_bytes,
        sub_id=body.get("sub_id"),
        clean_ip=body.get("clean_ip") or "",
        sni=body.get("sni") or "",
        host_header=body.get("host_header") or body.get("host") or "",
        fragment_packets=body.get("fragment_packets") or "",
        fragment_length=body.get("fragment_length") or "10-20",
        fragment_interval=body.get("fragment_interval") or "10-20",
        mux_enable=bool(body.get("mux_enable", False)),
        mux_concurrency=int(body.get("mux_concurrency") or 8),
        custom_uri=body.get("custom_uri") or "",
    )

    host = get_host(request)
    return {
        "uuid": uid,
        **link,
        "expired": False,
        "vless_link": vless_link_for_link(link, uid, host),
        "sub_url": f"https://{host}/p/{uid}",
        "raw_sub_url": f"https://{host}/sub/{uid}",
    }

@app.get("/api/links")
async def list_links(request: Request, _=Depends(require_auth)):
    host = get_host(request)
    async with LINKS_LOCK:
        snap = dict(LINKS)
    result = []
    for uid, d in snap.items():
        proto = d.get("protocol", DEFAULT_PROTOCOL)
        result.append({
            "uuid": uid,
            **d,
            "protocol": proto,
            "expired": is_link_expired(d),
            "vless_link": vless_link_for_link(d, uid, host),
            "sub_url": f"https://{host}/p/{uid}",
            "raw_sub_url": f"https://{host}/sub/{uid}",
            "connected_ips": len(unique_ips_for_uuid(uid)),
            "sub_id": d.get("sub_id"),
        })
    result.sort(key=lambda x: x["created_at"], reverse=True)
    return {"links": result}

@app.patch("/api/links/{uid}")
async def update_link(uid: str, request: Request, _=Depends(require_auth)):
    body = await request.json()
    async with LINKS_LOCK:
        if uid not in LINKS:
            raise HTTPException(status_code=404, detail="link not found")
        link = LINKS[uid]
        label = link.get("label")
        if "active" in body:
            link["active"] = bool(body["active"])
            log_activity("link", f"کانفیگ «{label}» {'فعال' if link['active'] else 'غیرفعال'} شد", "ok" if link["active"] else "warn")
        if "label" in body:
            link["label"] = str(body["label"])[:60]
        if "protocol" in body:
            proto = str(body.get("protocol") or DEFAULT_PROTOCOL).lower()
            link["protocol"] = proto if proto in PROTOCOLS else DEFAULT_PROTOCOL
        if "note" in body:
            link["note"] = str(body["note"])[:200]
        if "reset_usage" in body and body["reset_usage"]:
            link["used_bytes"] = 0
            log_activity("link", f"مصرف کانفیگ «{label}» ریست شد", "info")
        if "limit_value" in body:
            lv = float(body.get("limit_value") or 0)
            lu = body.get("limit_unit") or "GB"
            link["limit_bytes"] = 0 if lv <= 0 else parse_size_to_bytes(lv, lu)
        if "expires_days" in body:
            ed = int(body["expires_days"] or 0)
            link["expires_at"] = (datetime.now() + timedelta(days=ed)).isoformat() if ed > 0 else None
        if "fingerprint" in body:
            fp = str(body.get("fingerprint") or DEFAULT_FINGERPRINT).strip().lower()
            link["fingerprint"] = fp if fp in FINGERPRINTS else DEFAULT_FINGERPRINT
        if "alpn" in body:
            link["alpn"] = str(body.get("alpn") or "").strip()[:100]
        if "port" in body:
            try:
                p = int(body.get("port") or DEFAULT_PORT)
            except (TypeError, ValueError):
                p = DEFAULT_PORT
            link["port"] = p if p in ALLOWED_PORTS else DEFAULT_PORT
        if "ip_limit" in body:
            try:
                il = int(body.get("ip_limit") or 0)
            except (TypeError, ValueError):
                il = 0
            link["ip_limit"] = max(0, il)
        if "clean_ip" in body:
            link["clean_ip"] = str(body.get("clean_ip") or "").strip()
        if "sni" in body:
            link["sni"] = str(body.get("sni") or "").strip()
        if "host" in body or "host_header" in body:
            link["host"] = str(body.get("host_header") or body.get("host") or "").strip()
        if "fragment_packets" in body:
            link["fragment_packets"] = str(body.get("fragment_packets") or "").strip()
        if "fragment_length" in body:
            link["fragment_length"] = str(body.get("fragment_length") or "10-20").strip()
        if "fragment_interval" in body:
            link["fragment_interval"] = str(body.get("fragment_interval") or "10-20").strip()
        if "mux_enable" in body:
            link["mux_enable"] = bool(body["mux_enable"])
        if "mux_concurrency" in body:
            link["mux_concurrency"] = max(1, int(body.get("mux_concurrency") or 8))
        if "custom_uri" in body:
            link["custom_uri"] = str(body.get("custom_uri") or "").strip()
        if "speed_limit_value" in body:
            sv = float(body.get("speed_limit_value") or 0)
            su = body.get("speed_limit_unit") or "MBIT"
            link["speed_limit_bytes"] = 0 if sv <= 0 else parse_speed_to_bytes(sv, su)
            from speed_limit import reset_bucket
            reset_bucket(uid)
        if "sub_id" in body:
            link["sub_id"] = body["sub_id"] if body["sub_id"] else None
        if any(k in body for k in ("label", "protocol", "note", "limit_value", "expires_days", "fingerprint", "alpn", "port", "ip_limit", "speed_limit_value", "sub_id", "clean_ip", "sni", "host", "fragment_packets", "mux_enable")):
            log_activity("link", f"کانفیگ «{link['label']}» ویرایش شد", "info")

    asyncio.create_task(save_state())
    return {"ok": True}

@app.delete("/api/links/{uid}")
async def delete_link(uid: str, _=Depends(require_auth)):
    label = await remove_link(uid)
    if label is None:
        raise HTTPException(status_code=404, detail="link not found")
    return {"ok": True, "deleted": uid}

# ── Subscription Management APIs ──────────────────────────────────────────────
@app.post("/api/subs")
async def create_sub(request: Request, _=Depends(require_auth)):
    body = await request.json()
    lv = float(body.get("limit_value") or 0)
    lu = body.get("limit_unit") or "GB"
    limit_bytes = 0 if lv <= 0 else parse_size_to_bytes(lv, lu)
    
    exp_days = int(body.get("expires_days") or 0)
    expires_at = (datetime.now() + timedelta(days=exp_days)).isoformat() if exp_days > 0 else None
    
    try: ip_limit = int(body.get("ip_limit") or 0)
    except: ip_limit = 0
    try: sv = float(body.get("speed_limit_value") or 0)
    except: sv = 0
    su = body.get("speed_limit_unit") or "MBIT"
    speed_limit_bytes = 0 if sv <= 0 else parse_speed_to_bytes(sv, su)
    sub_id = secrets.token_hex(8)
    
    async with SUBS_LOCK:
        SUBS[sub_id] = {
            "label": str(body.get("label") or "اشتراک جدید")[:60],
            "limit_bytes": limit_bytes,
            "used_bytes": 0,
            "created_at": datetime.now().isoformat(),
            "expires_at": expires_at,
            "active": True,
            "ip_limit": max(0, ip_limit),
            "speed_limit_bytes": speed_limit_bytes,
            "note": str(body.get("note") or "")[:200],
        }
        
    if "links" in body and isinstance(body["links"], list):
        async with LINKS_LOCK:
            for uid in body["links"]:
                if uid in LINKS:
                    LINKS[uid]["sub_id"] = sub_id
                    
    asyncio.create_task(save_state())
    log_activity("sub", f"اشتراک «{SUBS[sub_id]['label']}» ساخته شد", "ok")
    return {"ok": True, "sub_id": sub_id, "sub": SUBS[sub_id]}

@app.get("/api/subs")
async def list_subs(request: Request, _=Depends(require_auth)):
    host = get_host(request)
    async with SUBS_LOCK:
        snap = dict(SUBS)
    result = []
    
    async with LINKS_LOCK:
        link_snap = dict(LINKS)
        
    for sid, s in snap.items():
        sub_links = [uid for uid, l in link_snap.items() if l.get("sub_id") == sid]
        sub_conn_count = sum(1 for c in connections.values() if c.get("uuid") in sub_links)
        
        result.append({
            "sub_id": sid,
            **s,
            "expired": is_sub_expired(s),
            "links_count": len(sub_links),
            "connections": sub_conn_count,
            "used_fmt": fmt_bytes(s.get("used_bytes", 0)),
            "limit_fmt": "∞" if s.get("limit_bytes", 0) == 0 else fmt_bytes(s["limit_bytes"]),
            "sub_url": f"https://{host}/p/{sid}",
            "raw_sub_url": f"https://{host}/sub/{sid}",
            "links": sub_links,
        })
    result.sort(key=lambda x: x.get("created_at") or "", reverse=True)
    return {"subs": result}

@app.patch("/api/subs/{sid}")
async def update_sub(sid: str, request: Request, _=Depends(require_auth)):
    body = await request.json()
    async with SUBS_LOCK:
        if sid not in SUBS:
            raise HTTPException(status_code=404, detail="sub not found")
        sub = SUBS[sid]
        
        if "active" in body: sub["active"] = bool(body["active"])
        if "label" in body: sub["label"] = str(body["label"])[:60]
        if "note" in body: sub["note"] = str(body["note"])[:200]
        if "reset_usage" in body and body["reset_usage"]: sub["used_bytes"] = 0
        if "limit_value" in body:
            lv = float(body.get("limit_value") or 0)
            lu = body.get("limit_unit") or "GB"
            sub["limit_bytes"] = 0 if lv <= 0 else parse_size_to_bytes(lv, lu)
        if "expires_days" in body:
            ed = int(body["expires_days"] or 0)
            sub["expires_at"] = (datetime.now() + timedelta(days=ed)).isoformat() if ed > 0 else None
        if "ip_limit" in body:
            try: il = int(body.get("ip_limit") or 0)
            except: il = 0
            sub["ip_limit"] = max(0, il)

        if "speed_limit_value" in body:
            sv = float(body.get("speed_limit_value") or 0)
            su = body.get("speed_limit_unit") or "MBIT"
            sub["speed_limit_bytes"] = 0 if sv <= 0 else parse_speed_to_bytes(sv, su)

        if "links" in body and isinstance(body["links"], list):
            async with LINKS_LOCK:
                for uid, l in LINKS.items():
                    if l.get("sub_id") == sid and uid not in body["links"]:
                        l["sub_id"] = None
                for uid in body["links"]:
                    if uid in LINKS:
                        LINKS[uid]["sub_id"] = sid
            
    asyncio.create_task(save_state())
    log_activity("sub", f"اشتراک «{sub.get('label')}» ویرایش شد", "info")
    return {"ok": True}

@app.delete("/api/subs/{sid}")
async def delete_sub(sid: str, _=Depends(require_auth)):
    async with SUBS_LOCK:
        if sid not in SUBS:
            raise HTTPException(status_code=404, detail="sub not found")
        label = SUBS[sid].get("label", sid)
        del SUBS[sid]
        
    async with LINKS_LOCK:
        for uid, l in LINKS.items():
            if l.get("sub_id") == sid:
                l["sub_id"] = None
            
    asyncio.create_task(save_state())
    log_activity("sub", f"اشتراک «{label}» حذف شد", "err")
    return {"ok": True, "deleted": sid}

# ── VLESS Transport Routes ────────────────────────────────────────────────────
# 1. VLESS gRPC Tunnel Route
from relay_grpc import grpc_tunnel

@app.post("/{service_name}/{method_name}")
@app.post("/{service_name}")
async def grpc_tunnel_route(service_name: str, request: Request, method_name: str = "Tun"):
    return await grpc_tunnel(request)

# 2. VLESS WebSocket Tunnel Route
from relay_vless import websocket_tunnel
app.add_api_websocket_route("/ws/{uuid}", websocket_tunnel)

# 3. XHTTP Ultra Router
from xhttp_siz10 import router as xhttp_router
app.include_router(xhttp_router)

# ── HTTP Proxy (Optional Utility) ─────────────────────────────────────────────
_HOP = {"connection","keep-alive","proxy-authenticate","proxy-authorization",
        "te","trailers","transfer-encoding","upgrade","content-encoding","content-length"}

@app.api_route("/proxy/{target_url:path}", methods=["GET","POST","PUT","DELETE","PATCH","HEAD","OPTIONS"])
async def http_proxy(target_url: str, request: Request):
    if not target_url.startswith("http"):
        target_url = "https://" + target_url
    try:
        body = await request.body()
        headers = {k: v for k, v in request.headers.items() if k.lower() not in _HOP and k.lower() != "host"}
        resp = await http_client.request(method=request.method, url=target_url, headers=headers, content=body)
        stats["total_bytes"] += len(resp.content)
        stats["total_requests"] += 1
        hourly_traffic[now_ir().strftime("%H:00")] += len(resp.content)
        return Response(content=resp.content, status_code=resp.status_code,
                        headers={k: v for k, v in resp.headers.items() if k.lower() not in _HOP})
    except Exception as exc:
        stats["total_errors"] += 1
        error_logs.append({"error": str(exc), "url": target_url, "time": datetime.now().isoformat()})
        raise HTTPException(status_code=502, detail=f"Proxy error: {exc}")

# ── Public Sub Pages (Web Dashboard per Subscription or Single Config) ─────────
@app.get("/p/{uuid_key}", response_class=HTMLResponse)
async def public_sub_page(uuid_key: str, request: Request):
    from pages import get_public_page_html
    async with SUBS_LOCK:
        sub_exists = uuid_key in SUBS
    async with LINKS_LOCK:
        link_exists = uuid_key in LINKS
        
    if not sub_exists and not link_exists:
        return HTMLResponse("<h2 style='font-family:sans-serif;padding:40px;color:#EF4444'>اشتراک یا کانفیگ پیدا نشد</h2>", status_code=404)
    return HTMLResponse(content=get_public_page_html(uuid_key))

@app.get("/api/public/sub/{uuid_key}")
async def public_sub_data(uuid_key: str, request: Request):
    host = get_host(request)
    
    # 1. Check if it's a Subscription
    async with SUBS_LOCK:
        sub = SUBS.get(uuid_key)
        
    if sub:
        async with LINKS_LOCK:
            sub_links = {uid: l for uid, l in LINKS.items() if l.get("sub_id") == uuid_key}
            
        links_out = []
        total_used = sub.get("used_bytes", 0)
        active_conns = 0
        
        for uid, l in sub_links.items():
            allowed = is_link_allowed(l)
            c_count = sum(1 for c in connections.values() if c.get("uuid") == uid)
            active_conns += c_count
            proto = l.get("protocol", DEFAULT_PROTOCOL)
            links_out.append({
                "uuid": uid,
                "label": l["label"],
                "active": allowed,
                "protocol": proto,
                "used_bytes": l.get("used_bytes", 0),
                "used_fmt": fmt_bytes(l.get("used_bytes", 0)),
                "limit_bytes": l.get("limit_bytes", 0),
                "limit_fmt": "∞" if l.get("limit_bytes", 0) == 0 else fmt_bytes(l["limit_bytes"]),
                "expires_at": l.get("expires_at"),
                "vless_link": vless_link_for_link(l, uid, host),
                "sub_url": f"https://{host}/p/{uid}",
                "connections": c_count,
                "ip_limit": l.get("ip_limit", 0),
                "speed_limit_bytes": l.get("speed_limit_bytes", 0),
            })
            
        return {
            "locked": False,
            "name": sub["label"],
            "desc": sub.get("note", ""),
            "sub_url": f"https://{host}/p/{uuid_key}",
            "raw_sub_url": f"https://{host}/sub/{uuid_key}",
            "active_connections": active_conns,
            "total_used_fmt": fmt_bytes(total_used),
            "limit_bytes": sub.get("limit_bytes", 0),
            "limit_fmt": "∞" if sub.get("limit_bytes", 0) == 0 else fmt_bytes(sub["limit_bytes"]),
            "expires_at": sub.get("expires_at"),
            "links": links_out,
        }

    # 2. Check if it's a Single Link
    async with LINKS_LOCK:
        link = LINKS.get(uuid_key)
    if not link:
        raise HTTPException(status_code=404, detail="not found")

    allowed = is_link_allowed(link)
    conn_count = sum(1 for c in connections.values() if c.get("uuid") == uuid_key)
    proto = link.get("protocol", DEFAULT_PROTOCOL)
    link_out = {
        "uuid": uuid_key,
        "label": link["label"],
        "active": allowed,
        "protocol": proto,
        "used_bytes": link.get("used_bytes", 0),
        "used_fmt": fmt_bytes(link.get("used_bytes", 0)),
        "limit_bytes": link.get("limit_bytes", 0),
        "limit_fmt": "∞" if link.get("limit_bytes", 0) == 0 else fmt_bytes(link["limit_bytes"]),
        "expires_at": link.get("expires_at"),
        "vless_link": vless_link_for_link(link, uuid_key, host),
        "sub_url": f"https://{host}/p/{uuid_key}",
        "raw_sub_url": f"https://{host}/sub/{uuid_key}",
        "connections": conn_count,
        "ip_limit": link.get("ip_limit", 0),
        "speed_limit_bytes": link.get("speed_limit_bytes", 0),
    }

    return {
        "locked": False,
        "name": link["label"],
        "desc": link.get("note", ""),
        "sub_url": f"https://{host}/p/{uuid_key}",
        "raw_sub_url": f"https://{host}/sub/{uuid_key}",
        "active_connections": conn_count,
        "total_used_fmt": fmt_bytes(link.get("used_bytes", 0)),
        "limit_bytes": link.get("limit_bytes", 0),
        "limit_fmt": "∞" if link.get("limit_bytes", 0) == 0 else fmt_bytes(link["limit_bytes"]),
        "expires_at": link.get("expires_at"),
        "links": [link_out],
    }

# ── HTML Pages (login + dashboard) ───────────────────────────────────────────
from pages import LOGIN_HTML, DASHBOARD_HTML

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    if await is_valid_session(request.cookies.get(SESSION_COOKIE)):
        return RedirectResponse(url="/dashboard")
    return HTMLResponse(content=LOGIN_HTML)

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    if not await is_valid_session(request.cookies.get(SESSION_COOKIE)):
        return RedirectResponse(url="/login")
    return HTMLResponse(content=DASHBOARD_HTML)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=CONFIG["port"], log_level="info", workers=1)
