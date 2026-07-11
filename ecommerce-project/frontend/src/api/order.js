import http from './axios';

export const createOrder = (userId) =>
  http.post('/orders', { userId });

export const getUserOrders = (userId) =>
  http.get(`/orders/user/${userId}`);

export const getOrder = (id) =>
  http.get(`/orders/${id}`);
