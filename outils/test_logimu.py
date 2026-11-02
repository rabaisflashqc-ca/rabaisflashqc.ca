#!/usr/bin/env python3
"""Test gratuit (sans clé) du serveur MCP Logimu : outil « shopping » sur amazon.ca. Écrit suivi/test_logimu.json."""
import json, urllib.request, pathlib, datetime
URL = "https://api.logimu.com/mcp"
H = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream", "User-Agent": "RabaisFlashQC-test"}
def post(body, sid=None):
    h = dict(H)
    if sid: h["Mcp-Session-Id"] = sid
    req = urllib.request.Request(URL, data=json.dumps(body).encode(), headers=h, method="POST")
    with urllib.request.urlopen(req, timeout=60) as r:
        txt = r.read().decode("utf-8", "replace"); sid2 = r.headers.get("Mcp-Session-Id")
    msgs = [json.loads(l[5:]) for l in txt.splitlines() if l.startswith("data:")] or ([json.loads(txt)] if txt.strip() else [])
    return msgs, sid2
out = {"quand": datetime.datetime.now(datetime.timezone.utc).isoformat()}
try:
    m, sid = post({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-03-26", "capabilities": {}, "clientInfo": {"name": "rfqc", "version": "1"}}})
    out["init"] = m
    try: post({"jsonrpc": "2.0", "method": "notifications/initialized"}, sid)
    except Exception as e: out["notif"] = str(e)
    m, _ = post({"jsonrpc": "2.0", "id": 2, "method": "tools/list"}, sid)
    tools = (m[0].get("result") or {}).get("tools", []) if m else []
    out["outils"] = [{"name": t["name"], "schema": t.get("inputSchema")} for t in tools]
    for i, q in enumerate(["B0BQPNMXQV", "B0CTNWBT1Z", "B0BS1QCFHX"]):
        args = {"q": q, "country": "ca"}
        m, _ = post({"jsonrpc": "2.0", "id": 10 + i, "method": "tools/call", "params": {"name": "shopping", "arguments": args}}, sid)
        out[f"shopping_{i}"] = m
except Exception as e:
    out["erreur"] = repr(e)
p = pathlib.Path(__file__).parent.parent / "suivi" / "test_logimu.json"
p.write_text(json.dumps(out, ensure_ascii=False, indent=1)[:400000])
print(json.dumps(out, ensure_ascii=False)[:3000])
