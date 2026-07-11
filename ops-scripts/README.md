# 云原生电商系统 - 运维操作手册

**适用场景**: 服务器环境已搭建完成，需要日常运维、代码更新、服务重启等操作  
**服务器**: 阿里云ECS (8.163.25.118)  
**最后更新**: 2026-07-12

---

## 📁 目录结构

```
ops-scripts/
├── deploy-all.sh              # 一键部署所有微服务 ⭐
├── deploy-single.sh           # 部署单个微服务 ⭐
├── check-status.sh            # 快速检查服务状态 ⭐
├── USAGE.md                   # 详细使用说明
└── README.md                  # 本文件（快速参考）
```

---

## 🔑 一、SSH免密登录（已配置完成）

✅ **SSH免密登录已成功配置**

### 快速连接服务器

```powershell
# Windows PowerShell - 直接连接服务器
ssh root@8.163.25.118
```

或者执行远程命令：

```powershell
# 执行单条命令
ssh root@8.163.25.118 "kubectl get pods"

# 执行多条命令
ssh root@8.163.25.118 "cd /root/ecommerce-project && git pull"

# 执行脚本文件
ssh root@8.163.25.118 'bash /root/deploy.sh'
```

### 验证免密登录

```powershell
# 测试连接（应该不需要输入密码）
ssh root@8.163.25.118 "echo 'SSH免密登录成功！'"
```

如果输出"SSH免密登录成功！"且没有提示输入密码，说明配置正常。

---

## 🚀 二、微服务重新部署流程

当代码有更新时，按照以下流程重新编译、打包、部署微服务。

### 前置条件

- ✅ SSH免密登录已配置
- ✅ Minikube集群正常运行
- ✅ 服务器上有项目代码 `/root/ecommerce-project/`

### 🎯 完整部署流程

**步骤1：上传最新代码到服务器**

```powershell
# 在项目根目录执行（包含 ecommerce-project 文件夹的目录）
scp -r ecommerce-project/* root@8.163.25.118:/root/ecommerce-project/

# 或者使用绝对路径（替换为您的实际路径）
scp -r D:\Project\paral\CourseProject\ecommerce-project\* root@8.163.25.118:/root/ecommerce-project/
```

⚠️ **注意**：只需上传代码文件，**不需要上传以下tar镜像文件**：
- `redis7.tar` - Redis镜像（服务器已配置阿里云镜像源自动拉取）
- `mysql8.tar` - MySQL镜像（服务器已配置阿里云镜像源自动拉取）
- `mongo6.tar` - MongoDB镜像（服务器已配置阿里云镜像源自动拉取）
- `nginx-alpine.tar` - Nginx镜像（服务器已配置阿里云镜像源自动拉取）

这些中间件镜像在服务器上会通过K8s自动从阿里云镜像仓库拉取，无需手动上传。

**步骤2：执行部署脚本**

```powershell
# 检查服务状态（部署前建议先检查）
ssh root@8.163.25.118 "/root/check-status.sh"

# 部署单个服务（例如cart-service）
ssh root@8.163.25.118 "/root/deploy-single.sh cart-service"

# 部署所有服务（谨慎使用，耗时较长）
ssh root@8.163.25.118 "/root/deploy-all.sh"
```

**步骤3：验证部署结果**

```powershell
# 再次检查服务状态
ssh root@8.163.25.118 "/root/check-status.sh"

# 查看服务日志
ssh root@8.163.25.118 "kubectl logs -f deployment/cart-service"
```

📖 **详细说明**: 查看 [USAGE.md](./USAGE.md) 获取每个脚本的参数说明和常见问题解答

---

## 🔍 三、服务状态检查

### 快速检查所有组件

使用 `check-status.sh` 脚本可以快速了解系统运行状态。

**使用方法：**

```powershell
ssh root@8.163.25.118 "/root/check-status.sh"
```

**检查内容包括：**
- Minikube集群状态
- 所有Pod运行状态
- Service配置
- 服务器资源使用情况（磁盘、内存）
- Docker容器状态
- 健康检查总结

---

### 常用检查命令

#### 检查Pod状态

```bash
# 查看所有Pod
ssh root@8.163.25.118 "kubectl get pods"

# 查看特定服务的Pod
ssh root@8.163.25.118 "kubectl get pods | grep cart-service"

# 查看Pod详细信息（包括事件）
ssh root@8.163.25.118 "kubectl describe pod <pod-name>"

# 查看Pod日志
ssh root@8.163.25.118 "kubectl logs -f <pod-name>"

# 查看最近100行日志
ssh root@8.163.25.118 "kubectl logs --tail=100 <pod-name>"
```

#### 检查Service配置

```bash
# 查看所有Service
ssh root@8.163.25.118 "kubectl get svc"

# 查看特定Service详情
ssh root@8.163.25.118 "kubectl describe svc web-service"
```

#### 检查Minikube状态

```bash
# 查看Minikube整体状态
ssh root@8.163.25.118 "minikube status"

# 查看Minikube IP
ssh root@8.163.25.118 "minikube ip"

# 查看Minikube日志
ssh root@8.163.25.118 "minikube logs"
```

#### 检查服务器资源

```bash
# 查看磁盘使用
ssh root@8.163.25.118 "df -h /"

# 查看内存使用
ssh root@8.163.25.118 "free -h"

# 查看CPU负载
ssh root@8.163.25.118 "top -bn1 | head -5"

# 查看Docker容器
ssh root@8.163.25.118 "docker ps"
```

#### 健康检查示例

```bash
# 检查所有微服务是否正常运行
ssh root@8.163.25.118 "kubectl get pods | grep -E 'cart-service|user-service|product-service|web-server'"

# 预期输出应该是：
# cart-service-xxx      1/1     Running
# user-service-xxx      1/1     Running
# product-service-xxx   1/1     Running
# web-server-xxx        1/1     Running

# 检查中间件是否正常
ssh root@8.163.25.118 "kubectl get pods | grep -E 'redis|mysql|mongodb'"

# 预期输出应该是：
# redis-xxx             1/1     Running
# mysql-xxx             1/1     Running
# mongodb-xxx           1/1     Running
```

---

## 📝 如何配置自己的SSH密钥（团队成员参考）

如果您是第一次使用此服务器，需要将自己的SSH公钥添加到服务器：

#### 步骤1：检查是否有SSH密钥

```powershell
# 查看是否有现有密钥
ls C:\Users\您的用户名\.ssh\id_rsa.pub
```

如果没有，生成新密钥：

```powershell
# 生成SSH密钥对
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
# 按Enter使用默认路径
# 按Enter设置空密码（方便自动化）
```

#### 步骤2：查看并复制公钥

```powershell
cat C:\Users\您的用户名\.ssh\id_rsa.pub
```

复制输出的全部内容（以`ssh-rsa`开头）。

#### 步骤3：联系管理员添加公钥

将您的公钥发送给项目管理员，由管理员在服务器上执行：

```bash
# 在服务器上执行（管理员操作）
echo "您的公钥内容" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

#### 步骤4：测试连接

```powershell
ssh root@8.163.25.118 "echo '连接成功！'"
```

---

### ⚠️ 注意事项

1. **私钥安全**：私钥文件（`id_rsa`）绝对不能上传到Git仓库或分享给他人
2. **PowerShell特殊字符**：在PowerShell中执行远程命令时，注意变量转义使用单引号
3. **首次使用**：如果是第一次连接，会提示确认主机指纹，输入`yes`即可

---

## ⚙️ 四、常用运维命令速查

### 1. 查看服务状态

```bash
# 查看所有Pod
ssh root@8.163.25.118 "kubectl get pods"

# 查看特定服务的Pod
ssh root@8.163.25.118 "kubectl get pods | grep cart-service"

# 查看Pod详细信息
ssh root@8.163.25.118 "kubectl describe pod <pod-name>"

# 查看Pod日志
ssh root@8.163.25.118 "kubectl logs -f <pod-name>"

# 查看最近100行日志
ssh root@8.163.25.118 "kubectl logs --tail=100 <pod-name>"
```

### 2. 重启服务

```bash
# 重启单个Deployment
ssh root@8.163.25.118 "kubectl rollout restart deployment/<service-name>"

# 重启所有微服务
ssh root@8.163.25.118 "kubectl rollout restart deployment/cart-service deployment/user-service deployment/product-service"

# 重启中间件
ssh root@8.163.25.118 "kubectl rollout restart deployment/redis deployment/mysql deployment/mongodb"
```

### 3. 查看资源使用情况

```bash
# 查看节点资源
ssh root@8.163.25.118 "kubectl top nodes"

# 查看Pod资源使用
ssh root@8.163.25.118 "kubectl top pods"

# 查看Minikube状态
ssh root@8.163.25.118 "minikube status"

# 查看Docker容器
ssh root@8.163.25.118 "docker ps"
```

### 4. 端口转发与访问

```bash
# 启动端口转发（在后台运行）
ssh root@8.163.25.118 "kubectl port-forward service/web-service 8080:80 &"

# 访问Web界面
# 浏览器打开: http://localhost:8080

# 停止端口转发
ssh root@8.163.25.118 "pkill -f 'kubectl port-forward'"
```

### 7. 数据库连接（只读操作）

```bash
# 连接MySQL（查询数据）
ssh root@8.163.25.118 "kubectl exec -it mysql-<pod-id> -- mysql -uroot -proot123"

# 连接Redis（查看缓存）
ssh root@8.163.25.118 "kubectl exec -it redis-<pod-id> -- redis-cli"

# 连接MongoDB（查询数据）
ssh root@8.163.25.118 "kubectl exec -it mongodb-<pod-id> -- mongosh"
```

⚠️ **注意**: 数据库操作请谨慎，避免执行DELETE、DROP等危险命令

### 6. 清理与重置

```bash
# 重启单个Deployment（安全操作）
ssh root@8.163.25.118 "kubectl rollout restart deployment/<service-name>"

# 查看Pod事件（排查问题）
ssh root@8.163.25.118 "kubectl describe pod <pod-name>"
```

⚠️ **注意**: 以下命令需要管理员权限，请勿随意执行：
- `kubectl delete pods --all` - 会删除所有Pod
- `minikube stop/delete` - 会停止或删除整个集群



---

## ⚠️ 注意事项

1. **日志监控**: 部署后立即检查日志，确认服务正常启动
2. **健康检查**: 确保所有Pod状态为 `1/1 Running` 才算部署成功
3. **脚本使用**: 优先使用提供的脚本，避免手动执行复杂命令
4. **问题反馈**: 遇到任何问题，及时联系管理员

---

## 📞 故障排查

### 问题1: Pod一直处于Pending状态

**原因**: 资源不足或镜像未加载

**解决**:
```bash
# 检查资源
ssh root@8.163.25.118 "kubectl describe pod <pod-name>"

# 检查镜像
ssh root@8.163.25.118 "minikube image ls | grep <image-name>"
```

### 问题2: Pod启动后 CrashLoopBackOff

**原因**: 应用启动失败（配置错误、依赖服务等）

**解决**:
```bash
# 查看日志
ssh root@8.163.25.118 "kubectl logs <pod-name>"

# 查看详细事件
ssh root@8.163.25.118 "kubectl describe pod <pod-name>"
```

### 问题3: 服务间无法通信

**原因**: Service配置错误或网络插件问题

**解决**:
```bash
# 检查Service
ssh root@8.163.25.118 "kubectl get svc"

# 测试连通性
ssh root@8.163.25.118 "kubectl exec <pod-name> -- curl http://<service-name>:<port>"
```

---

## 📚 相关文档

- [部署进度报告](../部署进度报告.md)
- [搭建指导手册](../搭建指导手册.md)
- [阿里云部署方案](../阿里云部署方案.md)

---

**维护者**: DevOps Team  
**联系方式**: 见项目README
