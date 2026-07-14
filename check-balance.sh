#!/bin/bash
MYSQL_POD=$(kubectl get pods -l app=mysql -o jsonpath="{.items[0].metadata.name}")

echo "=== 检查商家17的余额 ==="
kubectl exec -it $MYSQL_POD -- mysql -u root -prootpassword ecommerce -e "
SELECT id, username, role, balance
FROM users
WHERE id = 17;
" 2>/dev/null

echo ""
echo "=== 检查订单33的详情 ==="
kubectl exec -it $MYSQL_POD -- mysql -u root -prootpassword ecommerce -e "
SELECT id, user_id, merchant_id, total_price, status
FROM orders
WHERE id = 33;
" 2>/dev/null
