# CHANGELOG

## [1.1.0] - 2026-07-10

### 新增功能

- **用户认证安全**：密码使用 BCrypt 加密存储，替代明文存储
- **密码复杂度校验**：注册时校验密码最小长度（默认6位，可配置）
- **API 接口文档**：新增 `Docs/API接口文档.md`，包含路由总表、各服务接口详情、请求/响应示例
- **order-service 完整实现**：订单创建、用户订单列表、订单详情接口
- **JWT 鉴权过滤器**：cart-service、product-service、order-service 均添加 JWT 鉴权支持
- **跨服务 JWT 转发**：order-service 通过 RestTemplate 拦截器自动转发当前请求的 JWT Token

### 修复问题

- **product-service 公开接口被拦截**：商品浏览接口 (`/products/*`) 不再需要 JWT 鉴权
- **JJWT 废弃 API**：所有服务的 JWT 解析从 `setSigningKey()`/`getBody()` 升级为 `verifyWith()`/`getPayload()`
- **Spring Boot 包扫描范围**：所有服务的 `@SpringBootApplication` 添加 `scanBasePackages`，确保公共模块 `com.ecommerce.common` 被正确扫描
- **cart-service Lombok 编译失败**：移除 Lombok 依赖，改为手写 getter/setter
- **配置外部化**：默认余额、密码最小长度等配置项从硬编码迁移到 `application.yml`

### 变更文件

#### user-service
- `pom.xml` — 新增 spring-security-crypto 依赖
- `UserApplication.java` — 添加 scanBasePackages 配置
- `UserServiceImpl.java` — BCrypt 加密、密码长度校验、配置外部化
- `application.yml` — 新增 `app.user.password-min-length` 配置项
- 新增 `config/PasswordConfig.java` — BCryptPasswordEncoder Bean
- 新增 `config/JwtUtil.java` — JWT 工具类
- 新增 `dto/LoginResponse.java` — 登录响应 DTO
- 新增 `common/` — 公共模块（ApiResponse、BusinessException、GlobalExceptionHandler、PageResponse）

#### product-service
- `ProductApplication.java` — 添加 scanBasePackages 配置
- `application.yml` — 新增 `app.product.default-size` 配置项
- 新增 `config/JwtAuthFilter.java` — JWT 鉴权过滤器
- 新增 `config/WebConfig.java` — 过滤器注册（仅保护 `/reviews/*`）
- 新增 `common/` — 公共模块

#### cart-service
- `pom.xml` — 移除 Lombok 依赖
- `CartApplication.java` — 添加 scanBasePackages 配置
- `CartItemRequest.java` — 移除 @Data，改为手写 getter/setter
- `application.yml` — 新增 `app.cart.key-prefix`、`app.cart.ttl-days` 配置项
- 新增 `config/JwtAuthFilter.java` — JWT 鉴权过滤器
- 新增 `config/WebConfig.java` — 过滤器注册
- 新增 `config/RedisConfig.java` — Redis 序列化配置
- 新增 `dto/CartItem.java`、`dto/CartResponse.java` — 响应 DTO
- 新增 `common/` — 公共模块

#### order-service（新增）
- 完整的订单服务，包含 Controller、Service、Entity、Repository、DTO
- `config/AppConfig.java` — RestTemplate Bean + JWT Token 转发拦截器
- `config/JwtAuthFilter.java` — JWT 鉴权过滤器
- `config/WebConfig.java` — 过滤器注册
- `common/` — 公共模块

#### Docs
- 新增 `API接口文档.md` — 完整的前后端对接文档

---

## [1.0.0] - 2026-07-09

### 初始版本

- 基础项目结构搭建
- user-service：用户注册/登录、JWT 签发
- product-service：商品查询、评价管理（MongoDB）
- cart-service：购物车增删查（Redis）
- Docker + Minikube 部署配置
