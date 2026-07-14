#!/bin/bash
echo "=== Testing /products/merchant/{merchantId} API ==="

echo ""
echo "Test 1: merchantId=16"
curl -s 'http://localhost:30080/products/merchant/16' | python3 -c "
import sys, json
d = json.load(sys.stdin)
products = d.get('data', [])
print(f'   Total: {len(products)}')
if products:
    print(f'   First 3:')
    for p in products[:3]:
        print(f'   id={p[\"id\"]}, name={p[\"name\"][:30]}, merchantId={p.get(\"merchantId\")}')
"

echo ""
echo "Test 2: merchantId=5"
curl -s 'http://localhost:30080/products/merchant/5' | python3 -c "
import sys, json
d = json.load(sys.stdin)
products = d.get('data', [])
print(f'   Total: {len(products)}')
if products:
    print(f'   First 3:')
    for p in products[:3]:
        print(f'   id={p[\"id\"]}, name={p[\"name\"][:30]}, merchantId={p.get(\"merchantId\")}')
"
