#!/bin/bash
echo "=== 测试 addBalance API ==="

# 测试调用 add-balance API
echo "1. 调用 add-balance API (userId=17, amount=10)..."
curl -s -X PUT 'http://localhost:30080/users/17/add-balance?amount=10.00' \
  -H 'Content-Type: application/json'

echo ""
echo ""
echo "2. 检查商家17的余额..."
MYSQL_POD=$(kubectl get pods -l app=mysql -o jsonpath="{.items[0].metadata.name}")
kubectl exec -it $MYSQL_POD -- mysql -u root -prootpassword ecommerce -e "
SELECT id, username, role, balance
FROM users
WHERE id = 17;
" 2>/dev/null
