#!/bin/bash
echo "=== 测试商家21的商品（新创建的商家） ==="
curl -s 'http://localhost:30080/products/merchant/21' | python3 -c "
import sys, json
d = json.load(sys.stdin)
products = d.get('data', [])
print(f'商家21的商品数: {len(products)}')
if products:
    for p in products[:3]:
        print(f'  id={p[\"id\"]}, merchantId={p.get(\"merchantId\")}, name={p[\"name\"][:30]}')
else:
    print('  (无商品)')
"

echo ""
echo "=== 检查 MongoDB 中 merchantId 的范围 ==="
MONGO_POD=$(kubectl get pods -l app=mongodb -o jsonpath="{.items[0].metadata.name}")
kubectl exec -it $MONGO_POD -- mongosh --quiet --eval "
db = db.getSiblingDB('ecommerce');
print('merchantId 最小值: ' + db.products.find().sort({merchantId: 1}).limit(1).toArray()[0].merchantId);
print('merchantId 最大值: ' + db.products.find().sort({merchantId: -1}).limit(1).toArray()[0].merchantId);
"
