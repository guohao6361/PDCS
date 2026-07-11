const express = require('express');
const app = express();
app.use(express.json());

// ========== Mock 数据 ==========
let users = [
  { id: 1, username: 'test', password: '123456', balance: 10000 }
];
let nextUserId = 2;

const products = [
  { id: 1, name: 'MacBook Pro 14', price: 14999, stock: 50, category: 'Electronics', attributes: { brand: 'Apple', cpu: 'M3', ram: '18GB', storage: '512GB SSD' } },
  { id: 2, name: 'iPhone 15 Pro', price: 7999, stock: 100, category: 'Electronics', attributes: { brand: 'Apple', chip: 'A17 Pro', storage: '256GB' } },
  { id: 3, name: 'AirPods Pro 2', price: 1899, stock: 200, category: 'Electronics', attributes: { brand: 'Apple', type: 'TWS', anc: '主动降噪' } },
  { id: 4, name: 'iPad Air', price: 4799, stock: 80, category: 'Electronics', attributes: { brand: 'Apple', chip: 'M2', screen: '11英寸' } },
  { id: 5, name: 'Apple Watch S9', price: 2999, stock: 150, category: 'Wearables', attributes: { brand: 'Apple', chip: 'S9', display: '全天候显示' } },
  { id: 6, name: 'Sony WH-1000XM5', price: 2499, stock: 60, category: 'Audio', attributes: { brand: 'Sony', type: '头戴式', battery: '30小时' } },
  { id: 7, name: 'Samsung Galaxy S24', price: 5999, stock: 90, category: 'Electronics', attributes: { brand: 'Samsung', camera: '2亿像素', frame: '钛金属' } },
  { id: 8, name: 'Nintendo Switch OLED', price: 2599, stock: 120, category: 'Gaming', attributes: { brand: 'Nintendo', screen: '7英寸OLED', storage: '64GB' } },
  { id: 9, name: 'DJI Mini 4 Pro', price: 4788, stock: 40, category: 'Drones', attributes: { brand: 'DJI', video: '4K HDR', weight: '249g' } },
  { id: 10, name: 'Kindle Paperwhite', price: 999, stock: 300, category: 'E-Readers', attributes: { brand: 'Amazon', screen: '6.8英寸', ppi: '300ppi', waterproof: 'IPX8' } },
];

let reviews = [
  { id: 'r1', productId: 1, username: 'test', rating: 5, content: '性能强劲，屏幕惊艳，开发利器！' },
  { id: 'r2', productId: 1, username: 'test', rating: 4, content: '续航一般，其他都很满意。' },
  { id: 'r3', productId: 2, username: 'test', rating: 5, content: '拍照太强了，钛金属手感很好。' },
];
let nextReviewId = 4;

// cart: { [userId]: { [productId]: { productId, quantity } } }
let cart = {};

let orders = [];
let nextOrderId = 1;

// ========== 工具函数 ==========
function ok(data, message) {
  return { code: 200, message: message || 'success', data, timestamp: Date.now() };
}
function fail(code, message) {
  return { code, message, data: null, timestamp: Date.now() };
}

// ========== User API ==========
app.post('/users/register', (req, res) => {
  const { username, password } = req.body;
  if (!username || !password) return res.json(fail(400, '用户名和密码不能为空'));
  if (username.length < 2 || username.length > 20) return res.json(fail(400, '用户名长度需2-20字符'));
  if (password.length < 6 || password.length > 50) return res.json(fail(400, '密码长度需6-50字符'));
  if (users.find(u => u.username === username)) return res.json(fail(400, '用户名已存在'));
  const user = { id: nextUserId++, username, password, balance: 1000 };
  users.push(user);
  res.json(ok({ userId: user.id, username: user.username, balance: user.balance }));
});

app.post('/users/login', (req, res) => {
  const { username, password } = req.body;
  if (!username || !password) return res.json(fail(400, '用户名和密码不能为空'));
  const user = users.find(u => u.username === username && u.password === password);
  if (!user) return res.json(fail(400, '用户名或密码错误'));
  const token = Buffer.from(`user${user.id}:${Date.now()}`).toString('base64');
  res.json(ok({ token, userId: user.id, username: user.username, balance: user.balance }));
});

// ========== Product API ==========
app.get('/products', (req, res) => {
  const page = parseInt(req.query.page) || 0;
  const size = parseInt(req.query.size) || 10;
  const start = page * size;
  const content = products.slice(start, start + size);
  res.json(ok({
    content,
    page,
    size,
    totalElements: products.length,
    totalPages: Math.ceil(products.length / size)
  }));
});

app.get('/products/:id', (req, res) => {
  const product = products.find(p => p.id === parseInt(req.params.id));
  if (!product) return res.json(fail(404, '商品不存在'));
  res.json(ok(product));
});

// ========== Review API ==========
app.get('/reviews/:productId', (req, res) => {
  const list = reviews.filter(r => r.productId === parseInt(req.params.productId));
  res.json(ok(list));
});

app.post('/reviews', (req, res) => {
  const { productId, username, rating, content } = req.body;
  if (!productId || !rating || !content) return res.json(fail(400, '参数不完整'));
  if (rating < 1 || rating > 5) return res.json(fail(400, '评分需1-5'));
  const review = { id: 'r' + (nextReviewId++), productId, username: username || '匿名', rating, content };
  reviews.push(review);
  res.json(ok(review));
});

// ========== Cart API ==========
app.post('/cart/add', (req, res) => {
  const { userId, productId, quantity = 1 } = req.body;
  if (!userId || !productId) return res.json(fail(400, '参数不完整'));
  const product = products.find(p => p.id === productId);
  if (!product) return res.json(fail(404, '商品不存在'));
  if (!cart[userId]) cart[userId] = {};
  if (cart[userId][productId]) {
    cart[userId][productId].quantity += quantity;
  } else {
    cart[userId][productId] = { productId, quantity };
  }
  res.json(ok(null, '添加成功'));
});

app.get('/cart/:userId', (req, res) => {
  const userId = req.params.userId;
  const userCart = cart[userId] || {};
  const items = Object.values(userCart);
  res.json(ok({ userId: parseInt(userId), items }));
});

app.delete('/cart/:userId/:productId', (req, res) => {
  const { userId, productId } = req.params;
  if (cart[userId]) delete cart[userId][productId];
  res.json(ok(null, '移除成功'));
});

app.delete('/cart/:userId', (req, res) => {
  cart[req.params.userId] = {};
  res.json(ok(null, '清空成功'));
});

// ========== Order API ==========
app.post('/orders', (req, res) => {
  const { userId } = req.body;
  if (!userId) return res.json(fail(400, '参数不完整'));
  const user = users.find(u => u.id === userId);
  if (!user) return res.json(fail(404, '用户不存在'));
  const userCart = cart[userId] || {};
  const cartItems = Object.values(userCart);
  if (cartItems.length === 0) return res.json(fail(400, '购物车为空'));
  // 计算总价，生成订单明细
  let totalPrice = 0;
  const items = cartItems.map(ci => {
    const product = products.find(p => p.id === ci.productId);
    if (!product) return null;
    const subtotal = product.price * ci.quantity;
    totalPrice += subtotal;
    return { productId: ci.productId, productName: product.name, price: product.price, quantity: ci.quantity };
  }).filter(Boolean);
  if (user.balance < totalPrice) return res.json(fail(400, '余额不足'));
  // 扣减库存
  cartItems.forEach(ci => {
    const p = products.find(pp => pp.id === ci.productId);
    if (p) p.stock -= ci.quantity;
  });
  const order = {
    id: nextOrderId++,
    userId,
    totalPrice,
    status: 'CREATED',
    items,
    createdAt: new Date().toISOString()
  };
  orders.push(order);
  // 清空购物车
  cart[userId] = {};
  res.json(ok(order));
});

app.get('/orders/user/:userId', (req, res) => {
  const list = orders.filter(o => o.userId === parseInt(req.params.userId));
  list.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
  res.json(ok(list));
});

app.get('/orders/:id', (req, res) => {
  const order = orders.find(o => o.id === parseInt(req.params.id));
  if (!order) return res.json(fail(404, '订单不存在'));
  res.json(ok(order));
});

// ========== Payment API ==========
app.post('/orders/:id/pay', (req, res) => {
  const order = orders.find(o => o.id === parseInt(req.params.id));
  if (!order) return res.json(fail(404, '订单不存在'));
  if (order.status === 'PAID') return res.json(fail(400, '订单已支付'));
  if (order.status === 'CANCELLED') return res.json(fail(400, '订单已取消'));
  const user = users.find(u => u.id === order.userId);
  if (!user) return res.json(fail(404, '用户不存在'));
  if (user.balance < order.totalPrice) return res.json(fail(400, '余额不足'));
  // 扣款
  user.balance -= order.totalPrice;
  order.status = 'PAID';
  order.paidAt = new Date().toISOString();
  res.json(ok({ orderId: order.id, totalPrice: order.totalPrice, status: 'PAID', paidAt: order.paidAt, remainBalance: user.balance }, '支付成功'));
});

app.post('/orders/:id/cancel', (req, res) => {
  const order = orders.find(o => o.id === parseInt(req.params.id));
  if (!order) return res.json(fail(404, '订单不存在'));
  if (order.status === 'PAID') return res.json(fail(400, '已支付订单不可取消'));
  if (order.status === 'CANCELLED') return res.json(fail(400, '订单已取消'));
  // 恢复库存
  order.items.forEach(item => {
    const p = products.find(pp => pp.id === item.productId);
    if (p) p.stock += item.quantity;
  });
  order.status = 'CANCELLED';
  res.json(ok({ orderId: order.id, status: 'CANCELLED' }, '取消成功'));
});

// ========== 启动 ==========
const PORT = 9090;
app.listen(PORT, () => {
  console.log(`Mock server running at http://localhost:${PORT}`);
});
