const BACKEND_USER = 'http://localhost:8081';
const BACKEND_PRODUCT = 'http://localhost:8082';

export function getImageUrl(path) {
  if (!path) return '';
  if (path.startsWith('http')) return path;
  if (path.startsWith('/uploads/avatars')) return BACKEND_USER + path;
  if (path.startsWith('/uploads/products')) return BACKEND_PRODUCT + path;
  // MinIO 文件通过 user-service 的 /users/files/ 端点获取（相对路径，dev/prod 通用）
  if (path.startsWith('/files/')) return '/users' + path;
  return path;
}
