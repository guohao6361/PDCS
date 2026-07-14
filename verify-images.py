import sys, json
d = json.load(sys.stdin)
for p in d["data"]["content"][:5]:
    img_len = len(p.get("imageData", ""))
    status = "OK" if img_len > 5000 else "SMALL"
    print(f"{p['name'][:30]:30s} | {status} ({img_len} bytes)")
