import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// 浏览器导航请求（HTML）走 React 路由，API 请求走代理
const spaBypass = (req) => {
  if (req.headers.accept && req.headers.accept.includes('text/html')) {
    return '/index.html';
  }
  return undefined;
};

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/users':    { target: 'http://localhost:8081', changeOrigin: true, bypass: spaBypass },
      '/products': { target: 'http://localhost:8082', changeOrigin: true, bypass: spaBypass },
      '/reviews':  { target: 'http://localhost:8082', changeOrigin: true, bypass: spaBypass },
      '/cart':     { target: 'http://localhost:8083', changeOrigin: true, bypass: spaBypass },
      '/orders':   { target: 'http://localhost:8084', changeOrigin: true, bypass: spaBypass },
      '/uploads/avatars': { target: 'http://localhost:8081', changeOrigin: true },
      '/uploads/products': { target: 'http://localhost:8082', changeOrigin: true },
    }
  }
})
