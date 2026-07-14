const BACKEND_USER = 'http://localhost:8081';
const BACKEND_PRODUCT = 'http://localhost:8082';

export function getImageUrl(path) {
  if (!path) return '';
  if (path.startsWith('http')) return path;
  if (path.startsWith('/uploads/avatars')) return BACKEND_USER + path;
  if (path.startsWith('/uploads/products')) return BACKEND_PRODUCT + path;
  // MinIO 文件通过 Nginx 的 /files/ 路径访问（dev/prod 通用）
  return path;
}
