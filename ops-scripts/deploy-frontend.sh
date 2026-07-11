#!/bin/bash
# 前端Web服务部署脚本
# 用法: bash deploy-frontend.sh

set -e

echo "=========================================="
echo "部署前端Web服务"
echo "=========================================="
echo ""

# 1. 检查Minikube状态
echo "[1/5] 检查Minikube状态..."
if ! minikube status | grep -q "Running"; then
    echo "❌ Minikube未运行，请先启动Minikube"
    exit 1
fi
echo "✅ Minikube正在运行"
echo ""

# 2. 编译前端
echo "[2/5] 编译前端..."
cd /root/ecommerce-project/frontend

# 检查是否需要重新安装依赖
NEED_REINSTALL=false
if [ ! -d "node_modules" ]; then
    echo "   node_modules不存在，需要安装依赖..."
    NEED_REINSTALL=true
elif [ ! -f "node_modules/.package-lock.json" ]; then
    echo "   package-lock.json不匹配，需要重新安装依赖..."
    NEED_REINSTALL=true
fi

# 如果检测到需要重装，清理并重新安装
if [ "$NEED_REINSTALL" = true ]; then
    echo "   清理旧的node_modules..."
    rm -rf node_modules package-lock.json
    echo "   安装npm依赖（这可能需要几分钟）..."
    npm install
    if [ $? -ne 0 ]; then
        echo "❌ npm install失败，请检查网络连接或npm配置"
        exit 1
    fi
fi

# 执行构建
echo "   执行npm run build..."
npm run build
if [ $? -ne 0 ]; then
    echo "❌ 前端构建失败"
    exit 1
fi
echo "✅ 前端编译完成"
echo ""

# 3. 构建Docker镜像
echo "[3/5] 构建Docker镜像..."
docker build -t web-frontend:v1 .
echo "✅ 镜像构建完成"
echo ""

# 4. 加载镜像到Minikube
echo "[4/5] 加载镜像到Minikube..."
docker save web-frontend:v1 -o /tmp/web-frontend.tar
CONTAINER_ID=$(docker ps -q -f name=minikube)
docker cp /tmp/web-frontend.tar $CONTAINER_ID:/var/lib/docker/tmp/web-frontend.tar
docker exec $CONTAINER_ID docker load -i /var/lib/docker/tmp/web-frontend.tar
rm -f /tmp/web-frontend.tar
echo "✅ 镜像加载完成"
echo ""

# 5. 应用K8s配置
echo "[5/5] 应用K8s配置..."
kubectl apply -f /root/ecommerce-project/k8s/web-deployment.yaml
echo "✅ K8s配置已应用"
echo ""

# 6. 等待Pod就绪
echo "等待Pod就绪..."
kubectl rollout status deployment/web-server --timeout=120s
echo "✅ Pod已就绪"
echo ""

echo "=========================================="
echo "✅ 前端Web服务部署成功！"
echo "=========================================="
echo ""
echo "访问地址: http://<服务器IP>:30080"
echo ""
