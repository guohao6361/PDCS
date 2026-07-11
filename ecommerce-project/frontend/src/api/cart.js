import http from './axios';

export const addToCart = (userId, productId, quantity = 1) =>
  http.post('/cart/add', { userId, productId, quantity });

export const getCart = (userId) =>
  http.get(`/cart/${userId}`);

export const removeFromCart = (userId, productId) =>
  http.delete(`/cart/${userId}/${productId}`);

export const clearCart = (userId) =>
  http.delete(`/cart/${userId}`);

export const updateCartQuantity = (userId, productId, quantity) =>
  http.put(`/cart/${userId}/${productId}`, { quantity });

export const removeSelected = (userId, productIds) =>
  http.post(`/cart/${userId}/remove-selected`, { productIds });
