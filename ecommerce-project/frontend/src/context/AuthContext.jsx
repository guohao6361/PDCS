import { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { getUser } from '../api/user';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [initialized, setInitialized] = useState(false);

  // 刷新用户信息（从服务器获取最新数据）
  const refreshUser = useCallback(async () => {
    const currentUser = user || JSON.parse(localStorage.getItem('user') || 'null');
    if (!currentUser?.id) return;
    try {
      const data = await getUser(currentUser.id);
      const updated = { ...currentUser, ...data, id: data.id };
      setUser(updated);
      localStorage.setItem('user', JSON.stringify(updated));
      return updated;
    } catch (err) {
      console.error('刷新用户信息失败', err);
    }
  }, [user]);

  useEffect(() => {
    const savedToken = localStorage.getItem('token');
    const savedUser = localStorage.getItem('user');
    if (savedToken && savedUser) {
      setToken(savedToken);
      setUser(JSON.parse(savedUser));
    }
    setInitialized(true);
  }, []);

  // 初始化后自动刷新用户信息（获取最新余额等）
  useEffect(() => {
    if (initialized && user?.id) {
      refreshUser();
    }
  }, [initialized]);

  // 监听 401 事件，同步清除 React 状态
  useEffect(() => {
    const handleUnauthorized = () => {
      setUser(null);
      setToken(null);
    };
    window.addEventListener('auth:unauthorized', handleUnauthorized);
    return () => window.removeEventListener('auth:unauthorized', handleUnauthorized);
  }, []);

  const login = (token, userData) => {
    setToken(token);
    setUser(userData);
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(userData));
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  };

  const updateUser = (userData) => {
    setUser(userData);
    localStorage.setItem('user', JSON.stringify(userData));
  };

  return (
    <AuthContext.Provider value={{ user, token, initialized, login, logout, updateUser, refreshUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
