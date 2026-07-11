#!/bin/bash
# deploy-single.sh - 部署单个微服务
# 使用方法: 在服务器上直接执行 ./deploy-single.sh <service-name>
# 或从本地执行: ssh root@8.163.25.118 "/root/deploy-single.sh cart-service"
# 示例: ./deploy-single.sh cart-service

set -e  # 遇到错误立即退出

# 检查参数
if [ -z "$1" ]; then
    echo "❌ 请指定服务名称"
    echo "用法: ./deploy-single.sh <service-name>"
    echo "可用服务: cart-service, user-service, product-service"
    exit 1
fi

SERVICE_NAME=$1
PROJECT_DIR="/root/ecommerce-project"

echo "=========================================="
echo "部署服务: $SERVICE_NAME"
echo "=========================================="
echo ""

# 1. 检查Minikube状态
echo "[1/6] 检查Minikube状态..."
MINIKUBE_STATUS=$(minikube status | grep host | awk '{print $2}')
if [ "$MINIKUBE_STATUS" != "Running" ]; then
    echo "⚠️  Minikube未运行，正在启动..."
    minikube start --driver=docker --force
else
    echo "✅ Minikube正在运行"
fi
echo ""

# 2. Maven编译
echo "[2/6] 编译 $SERVICE_NAME ..."
cd $PROJECT_DIR/$SERVICE_NAME && mvn clean package -DskipTests
echo "✅ 编译完成"
echo ""

# 3. 构建Docker镜像
echo "[3/6] 构建Docker镜像..."
cd $PROJECT_DIR/$SERVICE_NAME && docker build -t ${SERVICE_NAME}:v1 .
echo "✅ 镜像构建完成"
echo ""

# 4. 加载镜像到Minikube
echo "[4/6] 加载镜像到Minikube..."
docker save ${SERVICE_NAME}:v1 -o /tmp/${SERVICE_NAME}.tar && \
  CONTAINER_ID=$(docker ps -q -f name=minikube) && \
  docker cp /tmp/${SERVICE_NAME}.tar $CONTAINER_ID:/var/lib/docker/tmp/${SERVICE_NAME}.tar && \
  docker exec $CONTAINER_ID docker load -i /var/lib/docker/tmp/${SERVICE_NAME}.tar
echo "✅ 镜像加载完成"
echo ""

# 5. 更新Deployment镜像并重启
echo "[5/6] 更新Deployment镜像..."
kubectl set image deployment/$SERVICE_NAME $SERVICE_NAME=${SERVICE_NAME}:v1
echo "✅ 镜像已更新为 ${SERVICE_NAME}:v1"
echo ""

# 6. 等待Pod就绪
echo "[6/6] 等待Pod就绪..."
kubectl rollout status deployment/$SERVICE_NAME --timeout=120s || {
    echo "⚠️  等待超时，请检查日志"
    kubectl logs -l app=$SERVICE_NAME --tail=50
    exit 1
}
echo ""

# 验证结果
echo "=========================================="
echo "验证部署结果"
echo "=========================================="
kubectl get pods | grep $SERVICE_NAME
echo ""

RUNNING_COUNT=$(kubectl get pods | grep $SERVICE_NAME | grep '1/1.*Running' | wc -l)
if [ "$RUNNING_COUNT" -gt 0 ]; then
    echo "✅ $SERVICE_NAME 部署成功！"
else
    echo "⚠️  $SERVICE_NAME 可能存在问题，请检查日志"
    echo "查看日志: kubectl logs -l app=$SERVICE_NAME"
fi
echo ""

echo "=========================================="
echo "✅ 部署完成！"
echo "=========================================="
