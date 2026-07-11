import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/users':    { target: 'http://localhost:8081', changeOrigin: true },
      '/products': { target: 'http://localhost:8082', changeOrigin: true },
      '/reviews':  { target: 'http://localhost:8082', changeOrigin: true },
      '/cart':     { target: 'http://localhost:8083', changeOrigin: true },
      '/orders':   { target: 'http://localhost:8084', changeOrigin: true },
    }
  }
})
