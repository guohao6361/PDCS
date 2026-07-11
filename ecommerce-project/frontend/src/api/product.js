import http from './axios';

export const getProducts = (page = 0, size = 10) =>
  http.get('/products', { params: { page, size } });

export const searchProducts = (keyword, page = 0, size = 10) =>
  http.get('/products/search', { params: { keyword, page, size } });

export const getProduct = (id) =>
  http.get(`/products/${id}`);

export const getReviews = (productId) =>
  http.get(`/reviews/${productId}`);

export const addReview = (data) =>
  http.post('/reviews', data);

// 商家/管理员 - 商品管理
export const uploadProductImage = (file) => {
  const formData = new FormData();
  formData.append('file', file);
  return http.post('/products/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
};

export const createProduct = (data) =>
  http.post('/products', data);

export const updateProduct = (id, data) =>
  http.put(`/products/${id}`, data);

export const deleteProduct = (id) =>
  http.delete(`/products/${id}`);

export const getMerchantProducts = (merchantId) =>
  http.get(`/products/merchant/${merchantId}`);
