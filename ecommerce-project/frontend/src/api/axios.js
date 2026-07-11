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
      handleUnauthorized();
      return Promise.reject(new Error('登录已过期，请重新登录'));
    }
    return Promise.reject(new Error(message));
  },
  error => {
    if (error.response && error.response.status === 401) {
      handleUnauthorized();
      return Promise.reject(new Error('登录已过期，请重新登录'));
    }
    return Promise.reject(new Error('网络异常，请检查连接'));
  }
);

function handleUnauthorized() {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
  // 通知 AuthContext 清除 React 状态
  window.dispatchEvent(new CustomEvent('auth:unauthorized'));
}

export default instance;
