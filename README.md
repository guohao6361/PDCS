# 云原生微服务电商系统

基于 Spring Boot + React 的云原生微服务电商系统，采用 Kubernetes 部署，包含完整的用户、商品、订单、购物车等核心功能模块。

## 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                        前端 (React + Vite)                   │
│                    nginx 反向代理 + 静态资源                   │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────┼──────────────────────────────────┐
│                     API 网关层 (nginx)                        │
│              /api/user  /api/product  /api/order  /api/cart  │
└──────┬──────────┬──────────┬──────────┬─────────────────────┘
       │          │          │          │
  ┌────▼───┐ ┌───▼────┐ ┌──▼───┐ ┌───▼────┐
  │ User   │ │Product │ │Order │ │ Cart   │
  │Service │ │Service │ │Svc   │ │Service │
  │ :8081  │ │ :8082  │ │:8083 │ │ :8084  │
  └───┬────┘ └───┬────┘ └──┬───┘ └───┬────┘
      │          │         │         │
  ┌───▼───┐ ┌───▼───┐ ┌──▼──┐ ┌───▼───┐
  │ MySQL │ │MongoDB│ │MySQL│ │ Redis │
  └───────┘ └───────┘ └─────┘ └───────┘
```

## 技术栈

### 后端
- **Spring Boot 2.7** - 微服务框架
- **Spring Data JPA / MongoDB** - 数据持久化
- **JWT** - 用户认证
- **Redis** - 缓存 & 会话管理
- **MinIO** - 对象存储（商品图片、用户头像）
- **Maven** - 依赖管理

### 前端
- **React 18** - UI 框架
- **Vite** - 构建工具
- **React Router** - 路由管理
- **Axios** - HTTP 客户端
- **nginx** - 静态资源服务 + 反向代理

### 部署
- **Docker** - 容器化
- **Kubernetes (Minikube)** - 容器编排
- **nginx** - 服务暴露

## 项目结构

```
PDCS/
├── ecommerce-project/
│   ├── frontend/              # React 前端
│   │   ├── src/
│   │   │   ├── api/           # API 接口封装
│   │   │   ├── components/    # 公共组件
│   │   │   ├── context/       # 全局状态 (AuthContext)
│   │   │   ├── pages/         # 页面组件
│   │   │   └── utils/         # 工具函数
│   │   ├── Dockerfile
│   │   └── nginx.conf
│   │
│   ├── user-service/          # 用户服务 (MySQL + JWT)
│   ├── product-service/       # 商品服务 (MongoDB)
│   ├── order-service/         # 订单服务 (MySQL)
│   ├── cart-service/          # 购物车服务 (Redis)
│   │
│   └── k8s/                   # Kubernetes 部署配置
│       ├── web-deployment.yaml
│       ├── user-deployment.yaml
│       ├── product-deployment.yaml
│       ├── order-deployment.yaml
│       ├── cart-deployment.yaml
│       ├── mysql-deployment.yaml
│       ├── mongodb-deployment.yaml
│       ├── redis-deployment.yaml
│       └── minio-deployment.yaml
│
├── Docs/                      # 项目文档
├── nginx/                     # nginx 配置
├── ops-scripts/               # 运维部署脚本
└── mock-server/               # Mock 服务
```

## 核心功能

### 用户模块
- 用户注册 / 登录 / JWT 认证
- 个人信息管理
- 收货地址管理
- 用户头像上传（MinIO）

### 商品模块
- 商品列表分页浏览（每页 16 个）
- 商品详情查看
- 商品图片展示（base64 编码）
- 商品搜索与筛选
- 商品评价

### 订单模块
- 购物车管理
- 订单创建 / 支付 / 查询
- 订单状态流转
- 商家订单处理

### 购物车模块
- 添加 / 修改 / 删除商品
- 数量调整
- 基于 Redis 的高性能缓存

### 管理后台
- 管理员仪表盘
- 商家仪表盘
- 商品管理（增删改查）
- 订单管理

## 快速开始

### 前置条件
- JDK 11+
- Node.js 16+
- Docker
- Minikube
- kubectl

### 本地开发

**启动前端：**
```bash
cd ecommerce-project/frontend
npm install
npm run dev
```

**启动后端服务：**
```bash
# 用户服务
cd ecommerce-project/user-service
mvn spring-boot:run

# 商品服务
cd ecommerce-project/product-service
mvn spring-boot:run

# 订单服务
cd ecommerce-project/order-service
mvn spring-boot:run

# 购物车服务
cd ecommerce-project/cart-service
mvn spring-boot:run
```

### Kubernetes 部署

```bash
# 启动 Minikube
minikube start

# 构建 Docker 镜像
cd ecommerce-project
docker build -t user-service:v1 -f user-service/Dockerfile user-service/
docker build -t product-service:v1 -f product-service/Dockerfile product-service/
docker build -t order-service:v1 -f order-service/Dockerfile order-service/
docker build -t cart-service:v1 -f cart-service/Dockerfile cart-service/
docker build -t web-frontend:v1 -f frontend/Dockerfile frontend/

# 导入镜像到 Minikube
docker save user-service:v1 | docker exec -i minikube docker load
docker save product-service:v1 | docker exec -i minikube docker load
# ... 其他服务同理

# 部署基础设施
kubectl apply -f k8s/mysql-deployment.yaml
kubectl apply -f k8s/mongodb-deployment.yaml
kubectl apply -f k8s/redis-deployment.yaml
kubectl apply -f k8s/minio-deployment.yaml

# 部署微服务
kubectl apply -f k8s/user-deployment.yaml
kubectl apply -f k8s/product-deployment.yaml
kubectl apply -f k8s/order-deployment.yaml
kubectl apply -f k8s/cart-deployment.yaml

# 部署前端
kubectl apply -f k8s/web-deployment.yaml

# 暴露服务
kubectl port-forward service/web-service 30080:80 --address 0.0.0.0
```

访问 http://localhost:30080 即可使用。

## 运维脚本

```bash
# 部署所有服务
bash ops-scripts/deploy-all.sh

# 部署单个服务
bash ops-scripts/deploy-single.sh <service-name>

# 部署前端
bash ops-scripts/deploy-frontend.sh

# 检查服务状态
bash ops-scripts/check-status.sh
```

## 数据说明

系统包含 82,000+ 条商品测试数据，涵盖 39 个真实商品（手机、笔记本、平板、耳机、家电等），每个商品包含多种规格变体。商品图片均从真实网站抓取并压缩存储。

## License

MIT
