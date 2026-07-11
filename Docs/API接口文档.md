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
| GET | /users/{id} | user-service(8081) | 是 | 查询用户信息 |
| PUT | /users/{id}/profile | user-service(8081) | 是 | 修改用户资料 |
| GET | /users/{id}/profile | user-service(8081) | 是 | 获取用户资料 |
| PUT | /users/{id}/password | user-service(8081) | 是 | 修改登录密码 |
| PUT | /users/{id}/pay-password | user-service(8081) | 是 | 修改支付密码 |
| POST | /users/{id}/reset-password | user-service(8081) | 是 | 重置密码 |
| POST | /users/{id}/avatar | user-service(8081) | 是 | 上传头像 |
| GET | /users/{id}/addresses | user-service(8081) | 是 | 获取地址列表 |
| POST | /users/{id}/addresses | user-service(8081) | 是 | 新增地址 |
| PUT | /users/{id}/addresses/{addressId} | user-service(8081) | 是 | 修改地址 |
| DELETE | /users/{id}/addresses/{addressId} | user-service(8081) | 是 | 删除地址 |
| PUT | /users/{id}/addresses/{addressId}/default | user-service(8081) | 是 | 设置默认地址 |
| DELETE | /users/{id}/self | user-service(8081) | 是 | 用户注销 |
| GET | /users/admin/users | user-service(8081) | 是(ADMIN) | 管理员查看所有用户 |
| PUT | /users/{id} | user-service(8081) | 是(ADMIN) | 管理员修改用户 |
| PUT | /users/{id}/role | user-service(8081) | 是(ADMIN) | 管理员修改角色 |
| DELETE | /users/{id} | user-service(8081) | 是(ADMIN) | 管理员删除用户 |
| GET | /products | product-service(8082) | 否 | 商品列表（分页） |
| GET | /products/{id} | product-service(8082) | 否 | 商品详情 |
| GET | /products/search | product-service(8082) | 否 | 商品搜索（按名称或分类） |
| POST | /products/upload | product-service(8082) | 是 | 上传商品图片 |
| POST | /products | product-service(8082) | 是(MERCHANT) | 商家发布商品 |
| PUT | /products/{id} | product-service(8082) | 是(MERCHANT) | 商家修改商品 |
| DELETE | /products/{id} | product-service(8082) | 是(MERCHANT) | 商家删除商品 |
| GET | /products/merchant/{merchantId} | product-service(8082) | 是 | 商家商品列表 |
| POST | /reviews | product-service(8082) | 是 | 发表评价 |
| GET | /reviews/{productId} | product-service(8082) | 是 | 查看商品评价列表 |
| POST | /cart/add | cart-service(8083) | 是 | 添加商品到购物车 |
| GET | /cart/{userId} | cart-service(8083) | 是 | 查询购物车 |
| PUT | /cart/{userId}/{productId} | cart-service(8083) | 是 | 更新购物车商品数量 |
| DELETE | /cart/{userId}/{productId} | cart-service(8083) | 是 | 移除购物车中某商品 |
| POST | /cart/{userId}/remove-selected | cart-service(8083) | 是 | 移除勾选商品 |
| DELETE | /cart/{userId} | cart-service(8083) | 是 | 清空购物车 |
| POST | /orders | order-service(8084) | 是 | 从购物车创建订单 |
| POST | /orders/selected | order-service(8084) | 是 | 勾选结算 |
| POST | /orders/{id}/pay | order-service(8084) | 是 | 支付订单（余额扣款） |
| POST | /orders/{id}/cancel | order-service(8084) | 是 | 取消订单（恢复库存） |
| PUT | /orders/{id}/status | order-service(8084) | 是 | 更新订单状态 |
| GET | /orders/user/{userId} | order-service(8084) | 是 | 用户订单列表 |
| GET | /orders/merchant/{merchantId} | order-service(8084) | 是(MERCHANT) | 商家订单列表 |
| GET | /orders/{id} | order-service(8084) | 是 | 订单详情 |
| GET | /orders/admin/orders | order-service(8084) | 是(ADMIN) | 管理员查看所有订单 |
| PUT | /orders/{id} | order-service(8084) | 是(ADMIN) | 管理员修改订单 |
| DELETE | /orders/{id} | order-service(8084) | 是(ADMIN) | 管理员删除订单 |

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
| username | string | 是 | 用户名，唯一，长度2-20字符 |
| password | string | 是 | 密码，长度6-50字符 |

**响应示例:**

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "userId": 1,
    "username": "testuser",
    "balance": 1000.00
  },
  "timestamp": 1783694484157
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| userId | int | 用户ID |
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

#### 3.1.3 管理员查看所有用户

- **GET** `/users/admin/users`
- **鉴权**: 需要 `Authorization: Bearer <token>`，且角色为 ADMIN

**响应示例:**

```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "id": 1,
      "username": "admin",
      "balance": 999999.00,
      "role": "ADMIN"
    },
    {
      "id": 2,
      "username": "testuser",
      "balance": 1000.00,
      "role": "USER"
    }
  ],
  "timestamp": 1783694720000
}
```

**业务错误:**
- `403` 需要管理员权限

---

#### 3.1.4 查询用户信息

- **GET** `/users/{id}`
- **鉴权**: 需要 `Authorization: Bearer <token>`

**路径参数:**

| 参数 | 类型 | 说明 |
|------|------|------|
| id | int | 用户ID |

**响应示例:**

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 2,
    "username": "testuser",
    "balance": 1000.00,
    "phone": "13800138000",
    "email": "test@example.com",
    "avatar": null,
    "role": "USER"
  },
  "timestamp": 1783751647891
}
```

---

#### 3.1.5 修改用户资料

- **PUT** `/users/{id}/profile`
- **鉴权**: 需要 `Authorization: Bearer <token>`

**请求体:**

```json
{
  "username": "newname",
  "phone": "13800138000",
  "email": "test@example.com"
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| username | string | 否 | 新用户名 |
| phone | string | 否 | 手机号 |
| email | string | 否 | 邮箱 |

---

#### 3.1.6 修改登录密码

- **PUT** `/users/{id}/password`
- **鉴权**: 需要 `Authorization: Bearer <token>`

**请求体:**

```json
{
  "oldPassword": "123456",
  "newPassword": "654321"
}
```

---

#### 3.1.7 修改支付密码

- **PUT** `/users/{id}/pay-password`
- **鉴权**: 需要 `Authorization: Bearer <token>`

**请求体:**

```json
{
  "oldPayPassword": "123456",
  "newPayPassword": "654321"
}
```

---

#### 3.1.8 重置密码

- **POST** `/users/{id}/reset-password`
- **鉴权**: 需要 `Authorization: Bearer <token>`

**请求体:**

```json
{
  "type": "LOGIN",
  "newPassword": "123456"
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| type | string | 是 | 密码类型：LOGIN（登录密码）或 PAY（支付密码） |
| newPassword | string | 是 | 新密码 |

---

#### 3.1.9 上传头像

- **POST** `/users/{id}/avatar`
- **鉴权**: 需要 `Authorization: Bearer <token>`
- **Content-Type**: multipart/form-data

**请求参数:**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| file | file | 是 | 头像图片文件 |

**响应示例:**

```json
{
  "code": 200,
  "message": "success",
  "data": "http://localhost:8081/uploads/avatars/2_1783751647891.jpg",
  "timestamp": 1783751647891
}
```

---

#### 3.1.10 新增地址

- **POST** `/users/{id}/addresses`
- **鉴权**: 需要 `Authorization: Bearer <token>`

**请求体:**

```json
{
  "receiverName": "Test",
  "phone": "13800138000",
  "province": "Beijing",
  "city": "Beijing",
  "district": "Chaoyang",
  "detailAddress": "Street 1",
  "isDefault": true
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| receiverName | string | 是 | 收件人姓名 |
| phone | string | 是 | 收件人手机号 |
| province | string | 是 | 省 |
| city | string | 是 | 市 |
| district | string | 是 | 区 |
| detailAddress | string | 是 | 详细地址 |
| isDefault | boolean | 否 | 是否默认地址 |

**响应示例:**

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "userId": 2,
    "receiverName": "Test",
    "phone": "13800138000",
    "province": "Beijing",
    "city": "Beijing",
    "district": "Chaoyang",
    "detailAddress": "Street 1",
    "isDefault": true
  },
  "timestamp": 1783751665224
}
```

---

#### 3.1.11 获取地址列表

- **GET** `/users/{id}/addresses`
- **鉴权**: 需要 `Authorization: Bearer <token>`

**响应示例:**

```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "id": 1,
      "userId": 2,
      "receiverName": "Test",
      "phone": "13800138000",
      "province": "Beijing",
      "city": "Beijing",
      "district": "Chaoyang",
      "detailAddress": "Street 1",
      "isDefault": true
    }
  ],
  "timestamp": 1783751836950
}
```

---

#### 3.1.12 修改地址

- **PUT** `/users/{id}/addresses/{addressId}`
- **鉴权**: 需要 `Authorization: Bearer <token>`

**请求体:** 同新增地址

---

#### 3.1.13 删除地址

- **DELETE** `/users/{id}/addresses/{addressId}`
- **鉴权**: 需要 `Authorization: Bearer <token>`

---

#### 3.1.14 设置默认地址

- **PUT** `/users/{id}/addresses/{addressId}/default`
- **鉴权**: 需要 `Authorization: Bearer <token>`

---

#### 3.1.15 用户注销

- **DELETE** `/users/{id}/self`
- **鉴权**: 需要 `Authorization: Bearer <token>`

---

#### 3.1.16 管理员修改用户

- **PUT** `/users/{id}`
- **鉴权**: 需要 `Authorization: Bearer <token>`，且角色为 ADMIN

**请求体:**

```json
{
  "username": "updated",
  "balance": 2000.00,
  "role": "MERCHANT"
}
```

---

#### 3.1.17 管理员修改角色

- **PUT** `/users/{id}/role`
- **鉴权**: 需要 `Authorization: Bearer <token>`，且角色为 ADMIN

**请求体:**

```json
{
  "role": "MERCHANT"
}
```

---

#### 3.1.18 管理员删除用户

- **DELETE** `/users/{id}`
- **鉴权**: 需要 `Authorization: Bearer <token>`，且角色为 ADMIN

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
| merchantId | int | 商家ID（新增） |
| description | string | 商品描述（新增） |
| imageUrl | string | 商品图片URL（新增） |
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

#### 3.2.3 商品搜索

- **GET** `/products/search?keyword={keyword}&page=0&size=10`
- **鉴权**: 无

**查询参数:**

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| keyword | string | 是 | - | 搜索关键词（匹配商品名称或分类） |
| page | int | 否 | 0 | 页码（从0开始） |
| size | int | 否 | 10 | 每页数量 |

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
    "totalElements": 1,
    "totalPages": 1
  },
  "timestamp": 1783694800000
}
```

---

#### 3.2.4 发表评价

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
| rating | int | 是 | 评分（1-5） |

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

#### 3.2.5 查看商品评价

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

#### 3.2.6 上传商品图片

- **POST** `/products/upload`
- **鉴权**: 需要 `Authorization: Bearer <token>`
- **Content-Type**: multipart/form-data

**请求参数:**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| file | file | 是 | 商品图片文件 |

**响应示例:**

```json
{
  "code": 200,
  "message": "success",
  "data": "http://localhost:8082/uploads/products/1_1783751647891.jpg",
  "timestamp": 1783751647891
}
```

---

#### 3.2.7 商家发布商品

- **POST** `/products`
- **鉴权**: 需要 `Authorization: Bearer <token>`，且角色为 MERCHANT 或 ADMIN

**请求体:**

```json
{
  "name": "新商品",
  "price": 999.00,
  "stock": 100,
  "category": "Electronics",
  "merchantId": 3,
  "description": "商品描述",
  "imageUrl": "http://localhost:8082/uploads/products/1.jpg",
  "attributes": {"color": "黑色"}
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | 是 | 商品名称 |
| price | decimal | 是 | 价格 |
| stock | int | 是 | 库存 |
| category | string | 否 | 分类 |
| merchantId | int | 是 | 商家ID |
| description | string | 否 | 商品描述 |
| imageUrl | string | 否 | 商品图片URL |
| attributes | object | 否 | 动态属性 |

---

#### 3.2.8 商家修改商品

- **PUT** `/products/{id}`
- **鉴权**: 需要 `Authorization: Bearer <token>`，且角色为 MERCHANT 或 ADMIN

**请求体:** 同发布商品，所有字段均为可选

---

#### 3.2.9 商家删除商品

- **DELETE** `/products/{id}`
- **鉴权**: 需要 `Authorization: Bearer <token>`，且角色为 MERCHANT 或 ADMIN

---

#### 3.2.10 商家商品列表

- **GET** `/products/merchant/{merchantId}`
- **鉴权**: 需要 `Authorization: Bearer <token>`

**路径参数:**

| 参数 | 类型 | 说明 |
|------|------|------|
| merchantId | int | 商家ID |

**响应示例:**

```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "id": 1,
      "name": "华为 Mate 60",
      "price": 6999.00,
      "stock": 50,
      "category": "Electronics",
      "merchantId": 3,
      "description": "商品描述",
      "imageUrl": "http://localhost:8082/uploads/products/1.jpg"
    }
  ],
  "timestamp": 1783751647891
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

#### 3.3.5 更新购物车商品数量

- **PUT** `/cart/{userId}/{productId}`
- **鉴权**: 需要

**路径参数:**

| 参数 | 类型 | 说明 |
|------|------|------|
| userId | long | 用户ID |
| productId | long | 商品ID |

**请求体:**

```json
{
  "quantity": 5
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| quantity | int | 是 | 新数量 |

**响应示例:**

```json
{
  "code": 200,
  "message": "数量更新成功",
  "data": null,
  "timestamp": 1783751647891
}
```

---

#### 3.3.6 移除勾选商品

- **POST** `/cart/{userId}/remove-selected`
- **鉴权**: 需要

**路径参数:**

| 参数 | 类型 | 说明 |
|------|------|------|
| userId | long | 用户ID |

**请求体:**

```json
{
  "productIds": [1, 2, 3]
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| productIds | array | 是 | 要移除的商品ID列表 |

**响应示例:**

```json
{
  "code": 200,
  "message": "勾选商品移除成功",
  "data": null,
  "timestamp": 1783751647891
}
```

**说明:** 用于勾选结算后清理购物车中的指定商品。

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
    "merchantId": 3,
    "addressId": null,
    "totalPrice": 13998.00,
    "status": "UNPAID",
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
| merchantId | int | 商家ID（新增） |
| addressId | int | 收货地址ID（新增） |
| totalPrice | decimal | 订单总价 |
| status | string | 订单状态（UNPAID） |
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

#### 3.4.2 支付订单

- **POST** `/orders/{id}/pay`
- **鉴权**: 需要

**说明:** 使用用户余额支付订单。系统会自动：
1. 校验订单状态（仅 UNPAID 可支付）
2. 校验15分钟超时（超时自动取消）
3. 验证支付密码（如果设置）
4. **扣减商品库存**（防止超卖）
5. 检查用户余额是否充足
6. 扣除用户余额
7. 更新订单状态为 PAID

**路径参数:**

| 参数 | 类型 | 说明 |
|------|------|------|
| id | long | 订单ID |

**请求体（可选）:**

```json
{
  "payPassword": "123456",
  "addressId": 1
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| payPassword | string | 否 | 支付密码 |
| addressId | int | 否 | 收货地址ID |

**响应示例:**

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "userId": 1,
    "merchantId": 3,
    "addressId": 1,
    "totalPrice": 13998.00,
    "status": "PAID",
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
  "timestamp": 1783694700000
}
```

**业务错误:**
- `400` 仅可支付UNPAID状态的订单
- `400` 订单已超时（超过15分钟），已自动取消
- `400` 支付密码错误
- `400` 余额不足
- `404` 订单不存在

---

#### 3.4.3 取消订单

- **POST** `/orders/{id}/cancel`
- **鉴权**: 需要

**说明:** 取消未支付的订单。系统会自动：
1. 校验订单状态（仅 UNPAID 可取消）
2. 更新订单状态为 CANCELLED
3. **恢复库存**（如果已扣减）

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
    "merchantId": 3,
    "addressId": null,
    "totalPrice": 499.00,
    "status": "CANCELLED",
    "items": [
      {
        "productId": 2,
        "productName": "机械键盘",
        "price": 499.00,
        "quantity": 1
      }
    ],
    "createdAt": "2026-07-10T22:43:54"
  },
  "timestamp": 1783694710000
}
```

**业务错误:**
- `400` 仅可取消UNPAID状态的订单
- `404` 订单不存在

---

#### 3.4.4 用户订单列表

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

#### 3.4.5 订单详情

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

#### 3.4.6 管理员查看所有订单

- **GET** `/orders/admin/orders`
- **鉴权**: 需要 `Authorization: Bearer <token>`，且角色为 ADMIN

**响应示例:**

```json
{
  "code": 200,
  "message": "success",
  "data": [
    {
      "id": 1,
      "userId": 2,
      "totalPrice": 13998.00,
      "status": "PAID",
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
  "timestamp": 1783694900000
}
```

**说明:** 返回所有用户的订单，按创建时间倒序排列。

**业务错误:**
- `403` 需要管理员权限

---

#### 3.4.7 勾选结算

- **POST** `/orders/selected`
- **鉴权**: 需要

**说明:** 根据勾选的商品ID列表从购物车创建订单。系统会自动：
1. 过滤购物车中勾选的商品
2. 查询商品价格并计算总价
3. 生成订单
4. 仅从购物车移除勾选的商品

**请求体:**

```json
{
  "userId": 1,
  "productIds": [1, 2, 3]
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| userId | int | 是 | 用户ID |
| productIds | array | 是 | 勾选的商品ID列表 |

**响应示例:** 同创建订单

---

#### 3.4.8 更新订单状态

- **PUT** `/orders/{id}/status`
- **鉴权**: 需要

**说明:** 完整状态机流转：
- UNPAID → PAID → SHIPPED → IN_TRANSIT → DELIVERED → COMPLETED
- UNPAID/PAID → CANCELLED

**路径参数:**

| 参数 | 类型 | 说明 |
|------|------|------|
| id | long | 订单ID |

**请求体:**

```json
{
  "status": "SHIPPED"
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| status | string | 是 | 新状态 |

**响应示例:** 同订单详情

**业务错误:**
- `400` 不允许从 X 变更为 Y

---

#### 3.4.9 商家订单列表

- **GET** `/orders/merchant/{merchantId}`
- **鉴权**: 需要 `Authorization: Bearer <token>`，且角色为 MERCHANT 或 ADMIN

**路径参数:**

| 参数 | 类型 | 说明 |
|------|------|------|
| merchantId | int | 商家ID |

**响应示例:** 同用户订单列表

**说明:** 返回该商家的所有订单，按创建时间倒序排列。

---

#### 3.4.10 管理员修改订单

- **PUT** `/orders/{id}`
- **鉴权**: 需要 `Authorization: Bearer <token>`，且角色为 ADMIN

**请求体:**

```json
{
  "status": "PAID"
}
```

---

#### 3.4.11 管理员删除订单

- **DELETE** `/orders/{id}`
- **鉴权**: 需要 `Authorization: Bearer <token>`，且角色为 ADMIN

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

### 4.3 订单状态说明

| 状态 | 含义 | 可执行操作 |
|------|------|------------|
| UNPAID | 待支付 | 支付、取消 |
| PAID | 已支付 | 发货、取消（需退款） |
| SHIPPED | 已发货 | 更新为运输中 |
| IN_TRANSIT | 运输中 | 更新为已送达 |
| DELIVERED | 已送达 | 更新为已完成 |
| COMPLETED | 已完成 | — |
| CANCELLED | 已取消 | — |

**状态流转规则:**
- UNPAID → PAID（支付）
- PAID → SHIPPED（发货）
- SHIPPED → IN_TRANSIT（运输中）
- IN_TRANSIT → DELIVERED（已送达）
- DELIVERED → COMPLETED（已完成）
- UNPAID/PAID → CANCELLED（取消）

### 4.4 错误响应示例

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

**角色说明:**
- **USER**: 普通用户，可访问用户、购物车、订单等个人相关接口
- **MERCHANT**: 商家，除普通用户权限外，还可发布/修改/删除商品，查看商家订单
- **ADMIN**: 管理员，拥有所有权限，可访问所有管理接口
- 默认注册的用户为 USER 角色
- 系统启动时自动创建 admin 账户（用户名: admin, 密码: admin123），角色为 ADMIN

### 5.5 典型业务流程

```
注册 → 登录(获取Token) → 浏览商品(无需Token) → 加入购物车 → 查看购物车 → 更新购物车数量 → 勾选结算(仅结算勾选商品) → 支付订单(验证支付密码+扣减库存+余额扣款) → 查看订单 → 更新订单状态(发货/运输/送达/完成)
```

**支付流程:**
```
创建订单(status=UNPAID, 不扣库存) → 进入支付页面 → 确认支付(验证支付密码+扣减库存+余额扣款, status=PAID) / 取消订单(恢复库存, status=CANCELLED)
```

**商家发布商品流程:**
```
商家登录 → 上传商品图片 → 发布商品(设置merchantId) → 查看商家商品列表 → 修改/删除商品
```

**收货地址管理流程:**
```
用户登录 → 新增收货地址 → 查看地址列表 → 设置默认地址 → 下单时选择地址(addressId)
```

**订单状态流转:**
```
UNPAID(待支付) → PAID(已支付) → SHIPPED(已发货) → IN_TRANSIT(运输中) → DELIVERED(已送达) → COMPLETED(已完成)
                ↘ CANCELLED(已取消)
```
