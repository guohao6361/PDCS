#!/bin/bash
MONGO_POD=$(kubectl get pods -l app=mongodb -o jsonpath="{.items[0].metadata.name}")
WEB_POD=$(kubectl get pods -l app=web-server -o jsonpath="{.items[0].metadata.name}")

echo "=== 验证 MongoDB 数据 ==="
kubectl exec $MONGO_POD -- mongosh /tmp/verify.js

echo "=== 验证图片文件 ==="
kubectl exec $WEB_POD -- ls -la /usr/share/nginx/html/images/products/ | head -10
IMG_COUNT=$(kubectl exec $WEB_POD -- ls /usr/share/nginx/html/images/products/ | wc -l)
echo "图片总数: $IMG_COUNT"

echo "=== 测试图片访问 ==="
FIRST_IMG=$(kubectl exec $WEB_POD -- ls /usr/share/nginx/html/images/products/ | head -1)
echo "第一张图片: $FIRST_IMG"
