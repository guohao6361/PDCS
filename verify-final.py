import sys, json
d = json.load(sys.stdin)
print(f"共 {d['data']['totalElements']} 个商品\n")
for p in d["data"]["content"][:8]:
    img_len = len(p.get("imageData", ""))
    status = "OK" if img_len > 1000 else "SMALL"
    print(f"[{p['id']}] {p['name'][:35]:35s} | {status} ({img_len} bytes)")
