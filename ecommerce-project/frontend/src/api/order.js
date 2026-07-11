import http from './axios';

// 创建订单
export const createOrder = (userId) =>
  http.post('/orders', { userId });

export const createSelectedOrder = (userId, productIds) =>
  http.post('/orders/selected', { userId, productIds });

// 订单操作
export const payOrder = (id, data) =>
  http.post(`/orders/${id}/pay`, data);

export const cancelOrder = (id) =>
  http.post(`/orders/${id}/cancel`);

export const updateOrderStatus = (id, status) =>
  http.put(`/orders/${id}/status`, { status });

// 查询订单
export const getUserOrders = (userId) =>
  http.get(`/orders/user/${userId}`);

export const getOrder = (id) =>
  http.get(`/orders/${id}`);

export const getMerchantOrders = (merchantId) =>
  http.get(`/orders/merchant/${merchantId}`);

export const getAllOrders = () =>
  http.get('/orders/admin/orders');

// 管理员 - 订单管理
export const updateOrder = (id, data) =>
  http.put(`/orders/${id}`, data);

export const deleteOrder = (id) =>
  http.delete(`/orders/${id}`);
