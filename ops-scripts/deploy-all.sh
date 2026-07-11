#!/bin/bash
# deploy-all.sh - 一键部署所有微服务
# 使用方法: 在服务器上直接执行 ./deploy-all.sh
# 或从本地执行: ssh root@8.163.25.118 "/root/deploy-all.sh"

set -e  # 遇到错误立即退出

PROJECT_DIR="/root/ecommerce-project"

echo "=========================================="
echo "开始部署所有微服务"
echo "=========================================="
echo ""

# 0. 检查环境
echo "[0/8] 检查环境..."
echo "✅ 环境检查正常"
echo ""

# 1. 检查Minikube状态
echo "[1/8] 检查Minikube状态..."
MINIKUBE_STATUS=$(minikube status | grep host | awk '{print $2}')
if [ "$MINIKUBE_STATUS" != "Running" ]; then
    echo "⚠️  Minikube未运行，正在启动..."
    minikube start --driver=docker --force
else
    echo "✅ Minikube正在运行"
fi
echo ""

# 2. 上传最新代码到服务器
echo "[2/8] 同步最新代码..."
echo "提示: 如果服务器上使用Git，请执行: cd $PROJECT_DIR && git pull"
echo ""

# 3. 部署cart-service
echo "[3/8] 部署cart-service..."
cd $PROJECT_DIR/cart-service && \
  mvn clean package -DskipTests && \
  docker build -t cart-service:v1 . && \
  docker save cart-service:v1 -o /tmp/cart-service.tar && \
  CONTAINER_ID=$(docker ps -q -f name=minikube) && \
  docker cp /tmp/cart-service.tar $CONTAINER_ID:/var/lib/docker/tmp/cart-service.tar && \
  docker exec $CONTAINER_ID docker load -i /var/lib/docker/tmp/cart-service.tar && \
  kubectl rollout restart deployment/cart-service
echo "✅ cart-service部署完成"
echo ""

# 4. 部署user-service
echo "[4/8] 部署user-service..."
cd $PROJECT_DIR/user-service && \
  mvn clean package -DskipTests && \
  docker build -t user-service:v1 . && \
  docker save user-service:v1 -o /tmp/user-service.tar && \
  CONTAINER_ID=$(docker ps -q -f name=minikube) && \
  docker cp /tmp/user-service.tar $CONTAINER_ID:/var/lib/docker/tmp/user-service.tar && \
  docker exec $CONTAINER_ID docker load -i /var/lib/docker/tmp/user-service.tar && \
  kubectl rollout restart deployment/user-service
echo "✅ user-service部署完成"
echo ""

# 5. 部署product-service
echo "[5/8] 部署product-service..."
cd $PROJECT_DIR/product-service && \
  mvn clean package -DskipTests && \
  docker build -t product-service:v1 . && \
  docker save product-service:v1 -o /tmp/product-service.tar && \
  CONTAINER_ID=$(docker ps -q -f name=minikube) && \
  docker cp /tmp/product-service.tar $CONTAINER_ID:/var/lib/docker/tmp/product-service.tar && \
  docker exec $CONTAINER_ID docker load -i /var/lib/docker/tmp/product-service.tar && \
  kubectl rollout restart deployment/product-service
echo "✅ product-service部署完成"
echo ""

# 6. 部署order-service
echo "[6/8] 部署order-service..."
cd $PROJECT_DIR/order-service && \
  mvn clean package -DskipTests && \
  docker build -t order-service:v1 . && \
  docker save order-service:v1 -o /tmp/order-service.tar && \
  CONTAINER_ID=$(docker ps -q -f name=minikube) && \
  docker cp /tmp/order-service.tar $CONTAINER_ID:/var/lib/docker/tmp/order-service.tar && \
  docker exec $CONTAINER_ID docker load -i /var/lib/docker/tmp/order-service.tar && \
  kubectl apply -f $PROJECT_DIR/k8s/order-deployment.yaml && \
  kubectl rollout restart deployment/order-service
echo "✅ order-service部署完成"
echo ""

# 7. 等待Pod就绪
echo "[7/9] 等待所有Pod就绪..."
echo "等待cart-service..."
kubectl rollout status deployment/cart-service --timeout=120s || echo "️  cart-service等待超时"

echo "等待user-service..."
kubectl rollout status deployment/user-service --timeout=120s || echo "⚠️  user-service等待超时"

echo "等待product-service..."
kubectl rollout status deployment/product-service --timeout=120s || echo "⚠️  product-service等待超时"

echo "等待order-service..."
kubectl rollout status deployment/order-service --timeout=120s || echo "⚠️  order-service等待超时"
echo ""

# 8. 验证部署结果
echo "[8/9] 验证部署结果..."
kubectl get pods | grep -E 'cart-service|user-service|product-service|order-service|web-server|redis|mysql|mongodb'
echo ""

# 9. 检查健康状态
echo "[9/9] 检查服务健康状态..."
RUNNING_COUNT=$(kubectl get pods | grep -E 'cart-service|user-service|product-service|order-service' | grep '1/1.*Running' | wc -l)
if [ "$RUNNING_COUNT" -eq 4 ]; then
    echo "✅ 所有微服务正常运行 (4/4)"
else
    echo "⚠️  部分服务异常，请检查日志: kubectl logs <pod-name>"
fi
echo ""

echo "=========================================="
echo "✅ 所有微服务部署完成！"
echo "=========================================="
echo ""
echo "下一步操作："
echo "1. 检查服务日志: kubectl logs -f deployment/<service-name>"
echo "2. 端口转发访问: kubectl port-forward service/web-service 8080:80 &"
echo "3. 浏览器访问: http://localhost:8080"
echo ""
