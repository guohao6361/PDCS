#!/bin/bash
MONGO_POD=$(kubectl get pods -l app=mongodb -o jsonpath="{.items[0].metadata.name}")

echo "=== 当前商品数据统计 ==="
kubectl exec -it $MONGO_POD -- mongosh --eval "
db = db.getSiblingDB('ecommerce');
var count = db.products.countDocuments();
var size = db.products.storageSize();
print('商品数量: ' + count);
print('数据大小: ' + (size/1024/1024).toFixed(2) + ' MB');

var sample = db.products.findOne();
if (sample) {
  print('\\n商品字段: ' + Object.keys(sample));
  print('示例数据: ' + JSON.stringify(sample).substring(0,800));
}
" 2>/dev/null
