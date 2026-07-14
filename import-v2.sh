#!/bin/bash
set -e
echo "=== 1. 获取 Pod 名称 ==="
MONGO_POD=$(kubectl get pods -l app=mongodb -o jsonpath="{.items[0].metadata.name}")
WEB_POD=$(kubectl get pods -l app=web-server -o jsonpath="{.items[0].metadata.name}")
echo "MongoDB: $MONGO_POD"
echo "Web: $WEB_POD"

echo "=== 2. 旧数据已删除，跳过 ==="

echo "=== 3. 复制图片到前端容器 ==="
kubectl exec $WEB_POD -- mkdir -p /usr/share/nginx/html/images/products
# 逐个复制图片文件
for f in /tmp/product_images/*; do
    fname=$(basename "$f")
    kubectl cp "$f" "$WEB_POD:/usr/share/nginx/html/images/products/$fname"
done
IMG_COUNT=$(kubectl exec $WEB_POD -- ls /usr/share/nginx/html/images/products/ | wc -l)
echo "图片数量: $IMG_COUNT"

echo "=== 4. 复制数据到 MongoDB ==="
kubectl cp /tmp/products_data.json $MONGO_POD:/tmp/products_data.json
echo "数据复制完成"

echo "=== 5. 导入数据 ==="
kubectl exec $MONGO_POD -- mongosh --eval "
const fs = require('fs');
db=db.getSiblingDB('ecommerce');
var raw = fs.readFileSync('/tmp/products_data.json', 'utf8');
var data=JSON.parse(raw);
var bulk=db.products.initializeUnorderedBulkOp();
var id=1;
for(var i=0;i<data.length;i++){var p=data[i];p._id=id;p.id=id;bulk.insert(p);id++;}
bulk.execute();
print('导入: '+data.length+' 条');
"

echo "=== 6. 验证 ==="
kubectl exec $MONGO_POD -- mongosh --eval "
db=db.getSiblingDB('ecommerce');
print('总数: '+db.products.countDocuments());
var s=db.products.stats();
print('数据大小: '+(s.dataSize/1024/1024).toFixed(2)+' MB');
print('存储大小: '+(s.storageSize/1024/1024).toFixed(2)+' MB');
var cats=db.products.aggregate([{\\$group:{_id:'\\$category',count:{\\$sum:1}}},{\\$sort:{count:-1}}]).toArray();
cats.forEach(function(c){print('  '+c._id+': '+c.count);});
var p=db.products.findOne();
print('示例图片: '+p.imageUrl);
print('示例名称: '+p.name);
"
echo "=== 完成 ==="
