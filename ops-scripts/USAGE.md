# 运维脚本使用说明

## 📁 脚本列表

本目录包含以下运维脚本：

1. **deploy-all.sh** - 一键部署所有微服务
2. **deploy-single.sh** - 部署单个微服务
3. **check-status.sh** - 快速检查所有服务状态

---

## 🚀 使用方法

### ✅ 推荐方式：从本地Windows执行（通过SSH）

这些脚本设计为**在服务器端直接执行**，您可以从本地Windows通过SSH调用它们。

#### 步骤1：上传脚本到服务器（首次使用）

```powershell
# 上传所有脚本
scp ops-scripts/*.sh root@8.163.25.118:/root/
```

#### 步骤2：赋予执行权限并运行

```powershell
# 一键部署所有服务
ssh root@8.163.25.118 "chmod +x /root/*.sh && /root/deploy-all.sh"

# 部署单个服务（例如cart-service）
ssh root@8.163.25.118 "/root/deploy-single.sh cart-service"

# 检查服务状态
ssh root@8.163.25.118 "/root/check-status.sh"
```

---

### 备选方式：登录服务器后直接执行

如果您已经通过SSH登录到服务器，可以直接执行：

```bash
# 登录服务器
ssh root@8.163.25.118

# 赋予执行权限（只需执行一次）
chmod +x /root/*.sh

# 执行脚本
/root/deploy-all.sh                    # 部署所有服务
/root/deploy-single.sh cart-service    # 部署单个服务
/root/check-status.sh                  # 检查状态
```

---

## 📋 脚本详细说明

### 1. deploy-all.sh - 一键部署所有微服务

**功能**：
- 检查SSH连接和Minikube状态
- 依次编译、构建、部署 cart-service、user-service、product-service
- 等待所有Pod就绪
- 验证部署结果

**使用场景**：
- 代码有重大更新，需要重新部署所有服务
- 首次部署或完全重置后重新部署

**注意事项**：
- ⚠️ 此脚本不会自动上传代码，请确保服务器上的代码是最新的
- ⚠️ 整个过程可能需要10-20分钟（取决于编译速度）
- ⚠️ 如果某个服务部署失败，脚本会停止并提示错误

**示例输出**：
```
==========================================
开始部署所有微服务
==========================================

[0/8] 检查SSH连接...
✅ SSH连接正常

[1/8] 检查Minikube状态...
✅ Minikube正在运行

[3/8] 部署cart-service...
✅ cart-service部署完成

...

==========================================
✅ 所有微服务部署完成！
==========================================
```

---

### 2. deploy-single.sh - 部署单个微服务

**功能**：
- 编译指定的微服务
- 构建Docker镜像并加载到Minikube
- 重启Deployment并等待就绪
- 验证部署结果

**使用场景**：
- 只修改了某个服务的代码
- 调试单个服务
- 快速迭代开发

**参数**：
- `<service-name>`: 服务名称（必填）
  - `cart-service` - 购物车服务
  - `user-service` - 用户服务
  - `product-service` - 商品服务

**示例**：
```bash
# 部署cart-service
ssh root@8.163.25.118 "/root/deploy-single.sh cart-service"

# 部署user-service
ssh root@8.163.25.118 "/root/deploy-single.sh user-service"

# 部署product-service
ssh root@8.163.25.118 "/root/deploy-single.sh product-service"
```

**注意事项**：
- ⚠️ 同样需要先确保服务器上的代码是最新的
- ⚠️ 编译时间约3-5分钟
- ⚠️ 如果部署失败，会自动显示最近50行日志

---

### 3. check-status.sh - 快速检查所有服务状态

**功能**：
- 检查Minikube集群状态
- 查看所有Pod运行状态
- 查看Service配置
- 检查服务器资源使用情况
- 健康检查总结

**使用场景**：
- 日常运维巡检
- 部署后验证
- 故障排查

**示例输出**：
```
==========================================
云原生电商系统 - 服务状态检查
==========================================

【1】Minikube集群状态
minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured

【2】Pod运行状态
NAME                               READY   STATUS    RESTARTS      AGE
cart-service-xxx                   1/1     Running   0             5m
user-service-xxx                   1/1     Running   0             5m
product-service-xxx                1/1     Running   0             5m
web-server-xxx                     1/1     Running   0             5m
redis-xxx                          1/1     Running   0             24h
mysql-xxx                          1/1     Running   0             24h
mongodb-xxx                        1/1     Running   0             24h

【6】健康检查总结
微服务运行数: 3/3
中间件运行数: 3/3
Web服务器: 1/1

✅ 所有服务正常运行！
```

---

## ⚠️ 重要提示

### 1. 代码同步

脚本**不会自动上传代码**到服务器。在执行部署前，请确保：

**方法A：使用Git（推荐）**
```bash
# 在服务器上执行
ssh root@8.163.25.118 "cd /root/ecommerce-project && git pull origin deployment"
```

**方法B：使用SCP上传**
```powershell
# 在本地Windows执行
scp -r ecommerce-project/* root@8.163.25.118:/root/ecommerce-project/
```

### 2. 镜像版本管理

当前脚本使用固定标签 `v1`。如果需要版本管理：

```bash
# 修改脚本中的镜像标签
# 将 v1 改为 v2, v3 等
docker build -t cart-service:v2 .
```

或者使用时间戳：
```bash
TAG=$(date +%Y%m%d%H%M%S)
docker build -t cart-service:$TAG .
```

### 3. 回滚操作

如果新版本有问题，可以回滚：

```bash
# 查看历史版本
ssh root@8.163.25.118 "kubectl rollout history deployment/cart-service"

# 回滚到上一个版本
ssh root@8.163.25.118 "kubectl rollout undo deployment/cart-service"

# 回滚到指定版本
ssh root@8.163.25.118 "kubectl rollout undo deployment/cart-service --to-revision=2"
```

### 4. 日志查看

部署后立即检查日志：

```bash
# 实时查看日志
ssh root@8.163.25.118 "kubectl logs -f deployment/cart-service"

# 查看最近100行
ssh root@8.163.25.118 "kubectl logs --tail=100 deployment/cart-service"

# 查看特定Pod的日志
ssh root@8.163.25.118 "kubectl logs <pod-name>"
```

---

## 🔧 常见问题

### Q1: 脚本执行时提示 "Permission denied"

**解决**：
```bash
ssh root@8.163.25.118 "chmod +x /root/*.sh"
```

### Q2: Maven编译失败

**可能原因**：
- 服务器内存不足
- Maven依赖下载失败

**解决**：
```bash
# 检查内存
ssh root@8.163.25.118 "free -h"

# 清理Maven缓存重试
ssh root@8.163.25.118 "cd /root/ecommerce-project/cart-service && rm -rf ~/.m2/repository && mvn clean package -DskipTests"
```

### Q3: Docker镜像加载失败

**可能原因**：
- Minikube容器ID获取失败
- 磁盘空间不足

**解决**：
```bash
# 检查Minikube状态
ssh root@8.163.25.118 "minikube status"

# 检查磁盘空间
ssh root@8.163.25.118 "df -h"

# 清理旧镜像
ssh root@8.163.25.118 "minikube ssh 'docker image prune -f'"
```

### Q4: Pod一直处于Pending状态

**解决**：
```bash
# 查看详细事件
ssh root@8.163.25.118 "kubectl describe pod <pod-name>"

# 检查资源限制
ssh root@8.163.25.118 "kubectl top nodes"
```

---

## 📞 技术支持

如有问题，请参考：
- [README.md](./README.md) - 完整运维手册
- [部署进度报告](../部署进度报告.md) - 部署历史和状态

---

**最后更新**: 2026-07-11  
**维护者**: DevOps Team
