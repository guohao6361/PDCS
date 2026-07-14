#!/bin/bash
MONGO_POD=$(kubectl get pods -l app=mongodb -o jsonpath='{.items[0].metadata.name}')
echo "MongoDB Pod: $MONGO_POD"

echo "=== 删除旧数据 ==="
cat > /tmp/clean.js << 'EOF'
db = db.getSiblingDB("ecommerce");
db.products.drop();
print("deleted");
EOF
kubectl cp /tmp/clean.js $MONGO_POD:/tmp/clean.js
kubectl exec $MONGO_POD -- mongosh --quiet /tmp/clean.js

for i in $(seq 1 28); do
    echo "=== 导入批次 $i/28 ==="
    # 复制 JSON 到 pod
    kubectl cp /tmp/batch_${i}.json $MONGO_POD:/tmp/batch_${i}.json
    
    # 创建导入脚本
    cat > /tmp/imp.js << JSEOF
const fs = require('fs');
db = db.getSiblingDB("ecommerce");
var raw = fs.readFileSync("/tmp/batch_${i}.json", "utf8");
var data = JSON.parse(raw);
db.products.insertMany(data);
print("batch ${i}: " + data.length + " imported");
JSEOF
    kubectl cp /tmp/imp.js $MONGO_POD:/tmp/imp.js
    kubectl exec $MONGO_POD -- mongosh --quiet /tmp/imp.js
done

echo "=== 验证 ==="
cat > /tmp/verify.js << 'EOF'
db = db.getSiblingDB("ecommerce");
var c = db.products.countDocuments();
var s = db.products.stats();
print("count: " + c);
print("size: " + (s.totalSize/1024/1024).toFixed(2) + " MB");
printjson(db.products.findOne());
EOF
kubectl cp /tmp/verify.js $MONGO_POD:/tmp/verify.js
kubectl exec $MONGO_POD -- mongosh --quiet /tmp/verify.js
