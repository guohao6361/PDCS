#!/bin/bash
echo "=== merchantId=7 ==="
curl -s 'http://localhost:30080/products/merchant/7' | python3 -c '
import sys, json
d = json.load(sys.stdin)
print("Count:", len(d["data"]))
for p in d["data"][:5]:
    mid = p.get("merchantId", "null")
    nm = p["name"][:20]
    print("  id=%s, merchantId=%s, name=%s" % (p["id"], mid, nm))
'

echo ""
echo "=== merchantId=1 ==="
curl -s 'http://localhost:30080/products/merchant/1' | python3 -c '
import sys, json
d = json.load(sys.stdin)
print("Count:", len(d["data"]))
for p in d["data"][:5]:
    mid = p.get("merchantId", "null")
    nm = p["name"][:20]
    print("  id=%s, merchantId=%s, name=%s" % (p["id"], mid, nm))
'
