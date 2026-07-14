#!/bin/bash
MONGO_POD=$(kubectl get pods -l app=mongodb -o jsonpath="{.items[0].metadata.name}")

echo "=== 将所有商品的 merchantId 设置为 null ==="
kubectl exec -it $MONGO_POD -- mongosh --quiet --eval "
db = db.getSiblingDB('ecommerce');
var result = db.products.updateMany(
  {},
  { \$set: { merchantId: null } }
);
print('修改完成！');
print('匹配文档数: ' + result.matchedCount);
print('修改文档数: ' + result.modifiedCount);
"

echo ""
echo "=== 验证修改结果 ==="
kubectl exec -it $MONGO_POD -- mongosh --quiet --eval "
db = db.getSiblingDB('ecommerce');
print('总商品数: ' + db.products.countDocuments());
print('merchantId 为 null 的商品数: ' + db.products.countDocuments({merchantId: null}));
print('merchantId 不为 null 的商品数: ' + db.products.countDocuments({merchantId: {\$ne: null}}));
"
