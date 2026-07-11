import http from './axios';

export const getProducts = (page = 0, size = 10) =>
  http.get('/products', { params: { page, size } });

export const getProduct = (id) =>
  http.get(`/products/${id}`);

export const getReviews = (productId) =>
  http.get(`/reviews/${productId}`);

export const addReview = (data) =>
  http.post('/reviews', data);
