#!/bin/bash
# check-status.sh - 快速检查所有服务状态
# 使用方法: 在服务器上直接执行 ./check-status.sh
# 或从本地执行: ssh root@8.163.25.118 "/root/check-status.sh"

echo "=========================================="
echo "云原生电商系统 - 服务状态检查"
echo "=========================================="
echo ""

# 1. Minikube集群状态
echo "【1】Minikube集群状态"
minikube status
echo ""

# 2. 所有Pod运行状态
echo "【2】Pod运行状态"
kubectl get pods
echo ""

# 3. Service配置
echo "【3】Service配置"
kubectl get svc
echo ""

# 4. 服务器资源使用情况
echo "【4】服务器资源使用"
echo '磁盘使用:' && df -h / | tail -1
echo '内存使用:' && free -h | grep Mem
echo ""

# 5. Docker容器状态
echo "【5】Docker容器"
docker ps --format 'table {{.Names}}\t{{.Status}}'
echo ""

# 6. 健康检查总结
echo "【6】健康检查总结"
MICROSERVICES=$(kubectl get pods | grep -E 'cart-service|user-service|product-service' | grep '1/1.*Running' | wc -l)
MIDDLEWARES=$(kubectl get pods | grep -E 'redis|mysql|mongodb' | grep '1/1.*Running' | wc -l)
WEB_SERVER=$(kubectl get pods | grep web-server | grep '1/1.*Running' | wc -l)

echo "微服务运行数: $MICROSERVICES/3"
echo "中间件运行数: $MIDDLEWARES/3"
echo "Web服务器: $WEB_SERVER/1"
echo ""

if [ "$MICROSERVICES" -eq 3 ] && [ "$MIDDLEWARES" -eq 3 ] && [ "$WEB_SERVER" -eq 1 ]; then
    echo "✅ 所有服务正常运行！"
else
    echo "⚠️  部分服务异常，请检查日志"
fi
echo ""

echo "=========================================="
echo "✅ 检查完成"
echo "=========================================="
