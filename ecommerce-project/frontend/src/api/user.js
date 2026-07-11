import http from './axios';

// 认证
export const login = (username, password) =>
  http.post('/users/login', { username, password });

export const register = (data) =>
  http.post('/users/register', data);

// 用户信息
export const getUser = (id) =>
  http.get(`/users/${id}`);

export const getProfile = (id) =>
  http.get(`/users/${id}/profile`);

export const updateProfile = (id, data) =>
  http.put(`/users/${id}/profile`, data);

export const uploadAvatar = (id, file) => {
  const formData = new FormData();
  formData.append('file', file);
  return http.post(`/users/${id}/avatar`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
};

// 密码管理
export const changePassword = (id, data) =>
  http.put(`/users/${id}/password`, data);

export const changePayPassword = (id, data) =>
  http.put(`/users/${id}/pay-password`, data);

export const resetPassword = (id, data) =>
  http.post(`/users/${id}/reset-password`, data);

// 收货地址
export const getAddresses = (id) =>
  http.get(`/users/${id}/addresses`);

export const createAddress = (id, data) =>
  http.post(`/users/${id}/addresses`, data);

export const updateAddress = (id, addressId, data) =>
  http.put(`/users/${id}/addresses/${addressId}`, data);

export const deleteAddress = (id, addressId) =>
  http.delete(`/users/${id}/addresses/${addressId}`);

export const setDefaultAddress = (id, addressId) =>
  http.put(`/users/${id}/addresses/${addressId}/default`);

// 用户注销
export const deleteSelf = (id) =>
  http.delete(`/users/${id}/self`);

// 管理员 - 用户管理
export const getAllUsers = () =>
  http.get('/users/admin/users');

export const updateUser = (id, data) =>
  http.put(`/users/${id}`, data);

export const updateUserRole = (id, role) =>
  http.put(`/users/${id}/role`, { role });

export const deleteUser = (id) =>
  http.delete(`/users/${id}`);
