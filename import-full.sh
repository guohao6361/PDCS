#!/bin/bash
set -e
MONGO_POD=$(kubectl get pods -l app=mongodb -o jsonpath="{.items[0].metadata.name}")
echo "MongoDB: $MONGO_POD"

echo "=== 检查磁盘空间 ==="
kubectl exec $MONGO_POD -- df -h /tmp

echo "=== 复制数据到 MongoDB Pod ==="
kubectl cp /tmp/products_full.json $MONGO_POD:/tmp/products_full.json
echo "复制完成"

echo "=== 删除旧数据 ==="
kubectl exec $MONGO_POD -- mongosh --eval "db=db.getSiblingDB('ecommerce');db.products.drop();print('已删除旧数据');"

echo "=== 导入数据 ==="
kubectl exec $MONGO_POD -- mongosh --eval "
const fs = require('fs');
db=db.getSiblingDB('ecommerce');
print('开始读取文件...');
var raw = fs.readFileSync('/tmp/products_full.json', 'utf8');
print('解析JSON...');
var data=JSON.parse(raw);
print('数据量: '+data.length);
var bulk=db.products.initializeUnorderedBulkOp();
var id=1;
for(var i=0;i<data.length;i++){var p=data[i];p._id=id;p.id=id;bulk.insert(p);id++;}
bulk.execute();
print('导入完成: '+data.length+' 条');
"

echo "=== 验证 ==="
kubectl cp /tmp/verify.js $MONGO_POD:/tmp/verify.js
kubectl exec $MONGO_POD -- mongosh /tmp/verify.js

echo "=== 完成 ==="
