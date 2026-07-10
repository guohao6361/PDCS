# 云原生微服务电商系统 — API 接口文档

## 一、概览

### 1.1 基础 URL

| 环境 | 基础 URL | 说明 |
|------|----------|------|
| 开发环境（直连） | `http://localhost:{port}` | 各服务独立端口 |
| 生产环境（Nginx 代理） | `http://{domain}` | 统一 80 端口，Nginx 按路径反向代理 |

各服务端口：

| 服务 | 端口 |
|------|------|
| user-service | 8081 |
| product-service | 8082 |
| cart-service | 8083 |
| order-service | 8084 |

### 1.2 统一响应格式

所有接口均返回 JSON，结构如下：

```json
{
  "code": 200,
  "message": "success",
  "data": { ... },
  "timestamp": 1783694484157
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 业务状态码，200=成功，非200=失败 |
| message | string | 提示信息 |
| data | T / null | 业务数据，失败时为 null |
| timestamp | long | 服务器时间戳（毫秒） |

### 1.3 鉴权方式

需要鉴权的接口须在请求头中携带 JWT Token：

```
Authorization: Bearer <token>
```

Token 通过 `/users/login` 接口获取。

---

## 二、路由总表

| 方法 | 路径 | 服务 | 鉴权 | 说明 |
|------|------|------|------|------|
| POST | /users/register | user-service(8081) | 否 | 用户注册 |
| POST | /users/login | user-service(8081) | 否 | 用户登录，返回 Token |
| GET | /products | product-service(8082) | 否 | 商品列表（分页） |
| GET | /products/{id} | product-service(8082) | 否 | 商品详情 |
| POST | /reviews | product-service(8082) | 是 | 发表评价 |
| GET | /reviews/{productId} | product-service(8082) | 是 | 查看商品评价列表 |
| POST | /cart/add | cart-service(8083) | 是 | 添加商品到购物车 |
| GET | /cart/{userId} | cart-service(8083) | 是 | 查询购物车 |
| DELETE | /cart/{userId}/{productId} | cart-service(8083) | 是 | 移除购物车中某商品 |
| DELETE | /cart/{userId} | cart-service(8083) | 是 | 清空购物车 |
| POST | /orders | order-service(8084) | 是 | 从购物车创建订单 |
| GET | /orders/user/{userId} | order-service(8084) | 是 | 用户订单列表 |
| GET | /orders/{id} | order-service(8084) | 是 | 订单详情 |

---

## 三、接口详情

### 3.1 用户服务 (user-service :8081)

#### 3.1.1 用户注册

- **POST** `/users/register`
- **鉴权**: 无

**请求体:**

```json
{
  "username": "testuser",
  "password": "123456"
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | 是 | 用户名，唯一，最长50字符 |
| password | string | 是 | 密码，最长100字符 |

**响应示例:**

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "username": "testuser",
    "balance": 1000.00
  },
  "timestamp": 1783694484157
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 用户ID |
| username | string | 用户名 |
| balance | decimal | 账户余额（注册赠送） |

**业务错误:**
- `400` 用户名已存在

---

#### 3.1.2 用户登录

- **POST** `/users/login`
- **鉴权**: 无

**请求体:**

```json
{
  "username": "testuser",
  "password": "123456"
}
```

**响应示例:**

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiJ9...",
    "userId": 1,
    "username": "testuser",
    "balance": 1000.00
  },
  "timestamp": 1783694491655
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| token | string | JWT Token，后续请求放入 `Authorization: Bearer <token>` |
| userId | int | 用户ID |
| username | string | 用户名 |
| balance | decimal | 账户余额 |

**业务错误:**
- `400` 用户不存在
- `400` 密码错误

---

### 3.2 商品服务 (product-service :8082)

#### 3.2.1 商品列表（分页）

- **GET** `/products?page=0&size=10`
- **鉴权**: 无

**查询参数:**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| page | int | 0 | 页码（从0开始） |
| size | int | 10 | 每页数量 |

**响应示例:**

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "content": [
      {
        "id": 1,
        "name": "华为 Mate 60",
        "price": 6999.00,
        "stock": 50,
        "category": "Electronics",
        "attributes": {
          "color": "雅川青",
          "storage": "512GB",
          "network": "5G"
        }
      }
    ],
    "page": 0,
    "size": 10,
    "totalElements": 3,
    "totalPages": 1
  },
  "timestamp": 1783694498345
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| content | array | 当前页商品列表 |
| page | int | 当前页码 |
| size | int | 每页数量 |
| totalElements | long | 总记录数 |
| totalPages | int | 总页数 |

**商品字段:**

| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 商品ID |
| name | string | 商品名称 |
| price | decimal | 价格 |
| stock | int | 库存数量 |
| category | string | 分类 |
| attributes | object | 动态属性（不同商品可有不同键值对） |

---

#### 3.2.2 商品详情

- **GET** `/products/{id}`
- **鉴权**: 无

**路径参数:**

| 参数 | 类型 | 说明 |
|------|------|------|
| id | int | 商品ID |

**响应示例:**

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "name": "华为 Mate 60",
    "price": 6999.00,
    "stock": 50,
    "category": "Electronics",
    "attributes": {
      "color": "雅川青",
      "storage": "512GB",
      "network": "5G"
    }
  },
  "timestamp": 1783694500000
}
```

**业务错误:**
- `404` 商品不存在

---

#### 3.2.3 发表评价

- **POST** `/reviews`
- **鉴权**: 需要 `Authorization: Bearer <token>`

**请求体:**

```json
{
  "productId": 1,
  "username": "testuser",
  "content": "非常好用！",
  "rating": 5
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| productId | int | 是 | 商品ID |
| username | string | 是 | 评价用户名 |
| content | string | 是 | 评价内容 |
| rating | int | 是 | 评分（建议1-5） |

**响应示例:**

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": "6691a2f3...",
    "productId": 1,
    "username": "testuser",
    "content": "非常好用！",
    "rating": 5
  },
  "timestamp": 1783694510000
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 评价ID（MongoDB 自动生成） |

---

#### 3.2.4 查看商品评价

- **GET** `/reviews/{productId}`
- **鉴权**: 需要 `Authorization: Bearer <token>`

**路径参数:**

| 参数 | 类型 | 说明 |
|------|------|------|
| productId | int | 商品ID |

**响应示例:**

```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "id": "6691a2f3...",
      "productId": 1,
      "username": "testuser",
      "content": "非常好用！",
      "rating": 5
    }
  ],
  "timestamp": 1783694520000
}
```

---

### 3.3 购物车服务 (cart-service :8083)

> 所有接口均需 `Authorization: Bearer <token>` 请求头

#### 3.3.1 添加商品到购物车

- **POST** `/cart/add`
- **鉴权**: 需要

**请求体:**

```json
{
  "userId": 1,
  "productId": 1,
  "quantity": 2
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| userId | long | 是 | 用户ID |
| productId | long | 是 | 商品ID |
| quantity | int | 是 | 数量 |

**响应示例:**

```json
{
  "code": 200,
  "message": "添加成功",
  "data": null,
  "timestamp": 1783694530000
}
```

---

#### 3.3.2 查询购物车

- **GET** `/cart/{userId}`
- **鉴权**: 需要

**路径参数:**

| 参数 | 类型 | 说明 |
|------|------|------|
| userId | long | 用户ID |

**响应示例:**

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "userId": 1,
    "items": [
      {
        "productId": 1,
        "quantity": 2
      },
      {
        "productId": 2,
        "quantity": 1
      }
    ]
  },
  "timestamp": 1783694540000
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| userId | long | 用户ID |
| items | array | 购物车商品列表 |
| items[].productId | long | 商品ID |
| items[].quantity | int | 数量 |

---

#### 3.3.3 移除购物车中某商品

- **DELETE** `/cart/{userId}/{productId}`
- **鉴权**: 需要

**路径参数:**

| 参数 | 类型 | 说明 |
|------|------|------|
| userId | long | 用户ID |
| productId | long | 商品ID |

**响应示例:**

```json
{
  "code": 200,
  "message": "移除成功",
  "data": null,
  "timestamp": 1783694550000
}
```

---

#### 3.3.4 清空购物车

- **DELETE** `/cart/{userId}`
- **鉴权**: 需要

**路径参数:**

| 参数 | 类型 | 说明 |
|------|------|------|
| userId | long | 用户ID |

**响应示例:**

```json
{
  "code": 200,
  "message": "清空成功",
  "data": null,
  "timestamp": 1783694560000
}
```

---

### 3.4 订单服务 (order-service :8084)

> 所有接口均需 `Authorization: Bearer <token>` 请求头

#### 3.4.1 创建订单

- **POST** `/orders`
- **鉴权**: 需要

**说明:** 从当前用户购物车创建订单。系统会自动：
1. 查询购物车内容
2. 查询各商品价格并校验库存
3. 计算总价，生成订单
4. 清空购物车

**请求体:**

```json
{
  "userId": 1
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| userId | int | 是 | 用户ID |

**响应示例:**

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "userId": 1,
    "totalPrice": 13998.00,
    "status": "CREATED",
    "items": [
      {
        "productId": 1,
        "productName": "华为 Mate 60",
        "price": 6999.00,
        "quantity": 2
      }
    ],
    "createdAt": "2026-07-10T22:43:54"
  },
  "timestamp": 1783694634610
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| id | long | 订单ID |
| userId | int | 用户ID |
| totalPrice | decimal | 订单总价 |
| status | string | 订单状态（CREATED） |
| items | array | 订单商品明细 |
| items[].productId | int | 商品ID |
| items[].productName | string | 商品名称 |
| items[].price | decimal | 单价 |
| items[].quantity | int | 数量 |
| createdAt | string | 创建时间 |

**业务错误:**
- `400` 购物车为空
- `400` 商品[xxx]库存不足
- `404` 商品不存在

---

#### 3.4.2 用户订单列表

- **GET** `/orders/user/{userId}`
- **鉴权**: 需要

**路径参数:**

| 参数 | 类型 | 说明 |
|------|------|------|
| userId | int | 用户ID |

**响应示例:**

```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "id": 1,
      "userId": 1,
      "totalPrice": 13998.00,
      "status": "CREATED",
      "items": [
        {
          "productId": 1,
          "productName": "华为 Mate 60",
          "price": 6999.00,
          "quantity": 2
        }
      ],
      "createdAt": "2026-07-10T22:43:54"
    }
  ],
  "timestamp": 1783694649872
}
```

**说明:** 返回结果按创建时间倒序排列。

---

#### 3.4.3 订单详情

- **GET** `/orders/{id}`
- **鉴权**: 需要

**路径参数:**

| 参数 | 类型 | 说明 |
|------|------|------|
| id | long | 订单ID |

**响应示例:**

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "userId": 1,
    "totalPrice": 13998.00,
    "status": "CREATED",
    "items": [
      {
        "productId": 1,
        "productName": "华为 Mate 60",
        "price": 6999.00,
        "quantity": 2
      }
    ],
    "createdAt": "2026-07-10T22:43:54"
  },
  "timestamp": 1783694660000
}
```

**业务错误:**
- `404` 订单不存在

---

## 四、错误码说明

### 4.1 HTTP 状态码

所有接口 HTTP 状态码均为 `200 OK`，通过响应体中的 `code` 字段区分业务结果。

### 4.2 业务状态码

| code | 含义 | 常见场景 |
|------|------|----------|
| 200 | 成功 | 正常响应 |
| 400 | 请求参数/业务错误 | 用户名已存在、密码错误、购物车为空、库存不足 |
| 401 | 未认证 | 未携带 Token、Token 无效或已过期 |
| 404 | 资源不存在 | 商品不存在、订单不存在 |
| 500 | 服务器内部错误 | 未捕获异常 |

### 4.3 错误响应示例

```json
{
  "code": 401,
  "message": "请先登录",
  "data": null,
  "timestamp": 1783694700000
}
```

```json
{
  "code": 400,
  "message": "用户名已存在",
  "data": null,
  "timestamp": 1783694710000
}
```

---

## 五、前端对接注意事项

### 5.1 跨域 (CORS)

各服务已配置允许跨域，开发环境前端可直接请求各端口。

### 5.2 开发环境建议

前端开发时直接请求各服务端口：

```javascript
const API = {
  user:    'http://localhost:8081',
  product: 'http://localhost:8082',
  cart:    'http://localhost:8083',
  order:   'http://localhost:8084'
};
```

### 5.3 生产环境

通过 Nginx 统一 80 端口反向代理，前端使用相对路径即可：

```
/users/*    → user-service:8081
/products/* → product-service:8082
/reviews/*  → product-service:8082
/cart/*     → cart-service:8083
/orders/*   → order-service:8084
```

### 5.4 鉴权流程

1. 调用 `/users/register` 注册
2. 调用 `/users/login` 登录，保存返回的 `token`
3. 后续所有需要鉴权的请求，在请求头中附加：
   ```
   Authorization: Bearer <token>
   ```
4. Token 过期后需重新登录获取新 Token

### 5.5 典型业务流程

```
注册 → 登录(获取Token) → 浏览商品(无需Token) → 加入购物车 → 查看购物车 → 创建订单(自动清空购物车) → 查看订单
```
