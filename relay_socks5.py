# relay_socks5.py
import asyncio
import secrets
from datetime import datetime
from fastapi import WebSocket, WebSocketDisconnect
from speed_limit import throttle

RELAY_BUF = 256 * 1024  # 256 KB

def _ws_client_ip(ws: WebSocket) -> str:
    from main import extract_client_ip
    host = ws.client.host if ws.client else None
    return extract_client_ip(ws.headers, host)

async def check_and_use(uid: str, n: int) -> bool:
    from main import LINKS, LINKS_LOCK, SUBS, stats, hourly_traffic, is_link_allowed, now_ir
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

async def relay_ws_to_tcp(ws: WebSocket, writer: asyncio.StreamWriter, conn_id: str, uid: str):
    from main import stats, connections
    try:
        while True:
            msg = await ws.receive()
            if msg["type"] == "websocket.disconnect":
                break
            data = msg.get("bytes") or (msg.get("text") or "").encode()
            if not data:
                continue
            if not await check_and_use(uid, len(data)):
                await ws.close(code=1008, reason="quota/disabled/unknown")
                break
            await throttle(uid, len(data))
            stats["total_requests"] += 1
            connections[conn_id]["bytes"] += len(data)
            writer.write(data)
            if writer.transport.get_write_buffer_size() > RELAY_BUF:
                await writer.drain()
    except Exception:
        pass
    finally:
        try:
            writer.write_eof()
        except Exception:
            pass

async def relay_tcp_to_ws(ws: WebSocket, reader: asyncio.StreamReader, conn_id: str, uid: str):
    from main import connections
    try:
        while True:
            data = await reader.read(RELAY_BUF)
            if not data:
                break
            if not await check_and_use(uid, len(data)):
                await ws.close(code=1008, reason="quota/disabled/unknown")
                break
            await throttle(uid, len(data))
            connections[conn_id]["bytes"] += len(data)
            await ws.send_bytes(data)
    except Exception:
        pass

async def handle_socks5_ws(ws: WebSocket, uid: str):
    from main import LINKS, LINKS_LOCK, is_link_allowed, connections, stats, error_logs
    await ws.accept()

    async with LINKS_LOCK:
        link = LINKS.get(uid)
        if not link or not is_link_allowed(link):
            await ws.close(code=1008, reason="Unauthorized/Expired/Disabled")
            return

    conn_id = secrets.token_hex(8)
    client_ip = _ws_client_ip(ws)
    connections[conn_id] = {
        "uuid": uid,
        "ip": client_ip,
        "connected_at": datetime.now().isoformat(),
        "last_connected_at": datetime.now().isoformat(),
        "bytes": 0,
        "type": "SOCKS5-WS",
    }

    try:
        # SOCKS5 Handshake - Greeting
        msg1 = await ws.receive()
        b1 = msg1.get("bytes") or (msg1.get("text") or "").encode()
        if not b1 or b1[0] != 0x05:
            await ws.close(code=1003, reason="Not SOCKS5")
            return
        
        # Respond No Auth required
        await ws.send_bytes(b"\x05\x00")

        # SOCKS5 Request
        msg2 = await ws.receive()
        b2 = msg2.get("bytes") or (msg2.get("text") or "").encode()
        if len(b2) < 7 or b2[0] != 0x05 or b2[1] != 0x01: # 0x01 = CONNECT
            await ws.close(code=1003, reason="Unsupported SOCKS5 cmd")
            return

        atyp = b2[3]
        pos = 4
        if atyp == 1: # IPv4
            target_host = ".".join(str(x) for x in b2[pos:pos+4])
            pos += 4
        elif atyp == 3: # Domain
            dlen = b2[pos]
            pos += 1
            target_host = b2[pos:pos+dlen].decode("utf-8", errors="ignore")
            pos += dlen
        elif atyp == 4: # IPv6
            ab = b2[pos:pos+16]
            pos += 16
            target_host = ":".join(f"{ab[i]:02x}{ab[i+1]:02x}" for i in range(0, 16, 2))
        else:
            await ws.close(code=1003, reason="Bad ATYP")
            return

        target_port = int.from_bytes(b2[pos:pos+2], "big")
        initial_data = b2[pos+2:]

        # Connect to destination
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(target_host, target_port), timeout=10.0
            )
        except Exception as e:
            # SOCKS5 error response
            await ws.send_bytes(b"\x05\x05\x00\x01\x00\x00\x00\x00\x00\x00")
            await ws.close()
            error_logs.append({"time": datetime.now().isoformat(), "msg": f"SOCKS5 dial {target_host}:{target_port} error: {e}"})
            return

        # SOCKS5 Success response
        await ws.send_bytes(b"\x05\x00\x00\x01\x00\x00\x00\x00\x00\x00")

        if initial_data:
            writer.write(initial_data)
            await writer.drain()

        # Run relay
        t1 = asyncio.create_task(relay_ws_to_tcp(ws, writer, conn_id, uid))
        t2 = asyncio.create_task(relay_tcp_to_ws(ws, reader, conn_id, uid))
        done, pending = await asyncio.wait([t1, t2], return_when=asyncio.FIRST_COMPLETED)
        for p in pending:
            p.cancel()

        try:
            writer.close()
            await writer.wait_closed()
        except Exception:
            pass

    except Exception as e:
        error_logs.append({"time": datetime.now().isoformat(), "msg": f"SOCKS5 WS error: {e}"})
    finally:
        connections.pop(conn_id, None)
