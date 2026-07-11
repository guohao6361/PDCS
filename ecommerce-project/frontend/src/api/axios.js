import axios from 'axios';

const instance = axios.create({
  timeout: 5000,
});

// 请求拦截器：自动附加 JWT
instance.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// 响应拦截器：统一解析 ApiResponse
instance.interceptors.response.use(
  response => {
    const { code, message, data } = response.data;
    if (code === 200) return data;
    if (code === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      setTimeout(() => {
        window.location.href = '/login';
      }, 100);
      return Promise.reject(new Error('登录已过期，请重新登录'));
    }
    return Promise.reject(new Error(message));
  },
  error => Promise.reject(new Error('网络异常，请检查连接'))
);

export default instance;
