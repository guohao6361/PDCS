import http from './axios';

export const payOrder = (orderId) =>
  http.post(`/orders/${orderId}/pay`);

export const cancelOrder = (orderId) =>
  http.post(`/orders/${orderId}/cancel`);
