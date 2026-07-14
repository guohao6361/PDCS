#!/bin/bash
set -e
MONGO_POD=$(kubectl get pods -l app=mongodb -o jsonpath="{.items[0].metadata.name}")
echo "MongoDB: $MONGO_POD"

echo "=== 删除旧数据 ==="
kubectl exec $MONGO_POD -- mongosh --eval "db=db.getSiblingDB('ecommerce');db.products.drop();print('已删除');"

# 分批导入
for i in 0 1 2 3 4 5 6; do
    BATCH_FILE="/tmp/products_batch_${i}.json"
    echo "=== 导入批次 $i ==="
    kubectl cp "$BATCH_FILE" "$MONGO_POD:/tmp/products_batch_${i}.json"
    kubectl exec $MONGO_POD -- mongosh --eval "
const fs = require('fs');
db=db.getSiblingDB('ecommerce');
var raw = fs.readFileSync('/tmp/products_batch_${i}.json', 'utf8');
var data=JSON.parse(raw);
var bulk=db.products.initializeUnorderedBulkOp();
for(var j=0;j<data.length;j++){var p=data[j];bulk.insert(p);}
bulk.execute();
print('批次$i导入: '+data.length+' 条');
"
    # 清理Pod内临时文件
    kubectl exec $MONGO_POD -- rm -f "/tmp/products_batch_${i}.json"
    echo "批次 $i 完成"
done

echo "=== 最终验证 ==="
kubectl cp /tmp/verify.js $MONGO_POD:/tmp/verify.js
kubectl exec $MONGO_POD -- mongosh /tmp/verify.js

echo "=== 全部完成 ==="
